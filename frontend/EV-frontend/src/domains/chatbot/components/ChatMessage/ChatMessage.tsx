import { useEffect, useRef } from 'react';
import { CHAT_PHASES, type ChatMessageProps } from "./types";

export function ChatMessage({ phase, text = '' }: ChatMessageProps) {
  const containerRef = useRef<HTMLDivElement>(null);

  // Auto-scroll automático hacia abajo cuando cambia el texto o la fase
  useEffect(() => {
    if (containerRef.current) {
      containerRef.current.scrollTop = containerRef.current.scrollHeight;
    }
  }, [text, phase]);

  const renderContent = () => {
    switch (phase) {
      case CHAT_PHASES.IDLE:
        return 'Listo para escuchar.';
      case CHAT_PHASES.LISTENING:
        return text ? `"${text}"` : 'Escuchándote...';
      case CHAT_PHASES.THINKING:
        return 'Pensando...';
      case CHAT_PHASES.SPEAKING:
        return text;
      default:
        return '';
    }
  };

  return (
    <div 
      ref={containerRef}
      aria-live="assertive" 
      className="ev-chat-container"
    >
      <p className={`ev-chat-text-${phase}`}>
        {renderContent()}
      </p>
    </div>
  );
}