import { useEffect, useState } from 'react';
import 'regenerator-runtime/runtime';
import { MIC_STATES, type MicState } from './domains/chatbot/components/MicrophoneButton/types';
import { CHAT_PHASES, type ChatPhase } from './domains/chatbot/components/ChatMessage/types';
import SpeechRecognition, { useSpeechRecognition } from 'react-speech-recognition'
import { LeftSidebar } from './domains/chatbot/layouts/LeftSidebar';
import { RightSidebar } from './domains/chatbot/layouts/RightSidebar';
import { InteractionCenter } from './domains/chatbot/layouts/InteractionCenter';

export function App() {
  const { 
    transcript,
    listening,
    resetTranscript,
    browserSupportsSpeechRecognition 
  } = useSpeechRecognition();  // Hook para manejar la transcripción de voz

  const [micState, setMicState] = useState<MicState>(MIC_STATES.READY);
  const [chatPhase, setChatPhase] = useState<ChatPhase>(CHAT_PHASES.IDLE);
  const [isOnline] = useState(true);
  const [aiResponse, setAiResponse] = useState<string>('');
  const [spokenText, setSpokenText] = useState<string>('');
  const [availableVoices, setAvailableVoices] = useState<SpeechSynthesisVoice[]>([]);

  // Este useEffect "caza" las voces de alta calidad en cuanto Edge las descarga
  useEffect(() => {
    const updateVoices = () => {
      const voices = window.speechSynthesis.getVoices();
      setAvailableVoices(voices);
    };

    updateVoices(); // Intento inicial
    window.speechSynthesis.onvoiceschanged = updateVoices; // Evento clave que avisa cuando llegan las de Azure
  }, []);

  useEffect(() => {
    if (listening) {
      setMicState(MIC_STATES.LISTENING);
      setChatPhase(CHAT_PHASES.LISTENING);
    } else if (!listening && transcript) {
      // Si se apagó y hay transcripción, enviamos al backend
      setMicState(MIC_STATES.READY);
      sendToBackend(transcript);
    } else if (!listening && !transcript && chatPhase === CHAT_PHASES.LISTENING) {
      // Si se apagó pero no se detectó voz, volvemos a reposo
      setMicState(MIC_STATES.READY);
      setChatPhase(CHAT_PHASES.IDLE);
    }
  }, [listening]);

  // 2. Función dinámica para enviar el texto transcrito
  const sendToBackend = async (userText: string) => {
    try {
      setChatPhase(CHAT_PHASES.THINKING);
      setAiResponse('');
      
      const response = await fetch('http://localhost:8000/chat/response', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ user_message: userText }),
      });

      
      if (!response.ok) {
        throw new Error(`Error HTTP: ${response.status}`);
      }

      const data = await response.json();
      
      setAiResponse(data.model_response);

      setChatPhase(CHAT_PHASES.SPEAKING);
      setMicState(MIC_STATES.IA_SPEAKING); // Cambia el botón para permitir interrumpir
      
      const utterThis = new SpeechSynthesisUtterance(data.model_response);
      utterThis.lang = 'es-ES';
            
      utterThis.voice = availableVoices.find(voice => 
        voice.lang.includes('es') && voice.name.includes('Natural') && voice.name.toLowerCase().includes('elvira')
      ) 
      // Si no encuentra a Elvira Natural, coge CUALQUIER voz "Natural" en español
      || availableVoices.find(voice => voice.lang.includes('es') && voice.name.includes('Natural')) 
      || availableVoices.find(voice => voice.lang.includes('es')) 
      || null;

      utterThis.onstart = () => {
        setSpokenText('');
      };
      //Cuando la voz pasa a la siguiente palabra, actualizamos el texto que se está pronunciando
      utterThis.onboundary = (event) => {
        const text = data.model_response.substring(event.charIndex);
        
        const boundaryIndex = text.indexOf(' ');
        
        const endOfWord = boundaryIndex === -1 
          ? data.model_response.length 
          : event.charIndex + boundaryIndex;
          
        setSpokenText(data.model_response.substring(0, endOfWord));
      };

      utterThis.onend = () => {
        setTimeout(() => {
          setMicState(MIC_STATES.READY);
          setChatPhase(CHAT_PHASES.IDLE);
          setAiResponse('');
          setSpokenText('');
        }, 1500);
      };

      window.speechSynthesis.speak(utterThis);

    } catch (error) {
      console.error("Error al conectar con el backend:", error);
      setAiResponse("Error de conexión con el núcleo de E.V.");
      setChatPhase(CHAT_PHASES.SPEAKING);
      setMicState(MIC_STATES.READY);
    }
  };

  // 3. Control del Click del Botón
  const handleMicClick = () => {
    if (micState === MIC_STATES.IA_SPEAKING) {
      // Si la IA está hablando y pulsamos, la interrumpimos y volvemos a reposo
      
      window.speechSynthesis.cancel();
      setMicState(MIC_STATES.READY);
      setChatPhase(CHAT_PHASES.IDLE);
      setAiResponse('');
      return;
    }

    if (!listening) {
      resetTranscript(); // Limpiamos transcripciones anteriores
      setAiResponse('');
      SpeechRecognition.startListening({ continuous: false, language: 'es-ES' });
    } else {
      SpeechRecognition.stopListening(); // Apagar el micro dispara el useEffect
    }
  };

  const openConfigModal = () => {
    alert('Abriendo el modal del dominio de configuration');
  };

  if (!browserSupportsSpeechRecognition) {
    return <div className="text-symbiote-red p-8 flex justify-center items-center h-screen">Tu navegador no soporta la Web Speech API. Abre la app en Chrome o Edge.</div>;
  }

  // 4. Determinar qué texto mostrar en pantalla
  const displayText = chatPhase === CHAT_PHASES.LISTENING ? transcript : 
                      chatPhase === CHAT_PHASES.SPEAKING ? spokenText : '';

  return (
    <div className="ev-layout">
      <LeftSidebar isOnline={isOnline} />
      
      <InteractionCenter 
        micState={micState} 
        chatPhase={chatPhase} 
        displayText={displayText} 
        onMicClick={handleMicClick} 
      />
      
      <RightSidebar onConfigClick={openConfigModal} />
    </div>
  );
}