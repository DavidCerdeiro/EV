export const MIC_STATES = {
  READY: 'ready',            // 1. Listo para hablar
  LISTENING: 'listening',    // 2. Escuchando
  IA_SPEAKING: 'ia_speaking', // 3. Stop (IA hablando)
  THINKING: 'thinking'       // 4. Pensando
};

export type MicState = typeof MIC_STATES[keyof typeof MIC_STATES];

export interface MicrophoneButtonProps {
  currentState?: MicState;
  onClick: () => void; 
}