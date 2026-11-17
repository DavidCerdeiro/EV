import React from 'react';

export function InputBox({ 
  id, 
  labelText, 
  placeholder, 
  value,
  onChange,
  autoFocus,
  actionButton,
  error // Nueva propiedad para mensajes de error
}: { 
  id: string; 
  labelText: string; 
  placeholder: string;
  value: string;
  onChange: (e: React.ChangeEvent<HTMLInputElement>) => void; // Vuelve a ser obligatorio
  autoFocus?: boolean;
  actionButton?: React.ReactNode;
  error?: string;
}) {
  return (
    <div className="ev-input-group">
      <label htmlFor={id} className="ev-label">
        {labelText}
      </label>
      <div className="relative flex items-center">
        <input 
          type="text" 
          id={id} 
          value={value}
          onChange={onChange}
          placeholder={placeholder}
          autoFocus={autoFocus}
          aria-label={labelText}
          aria-invalid={!!error}
          className={`ev-input w-full ${actionButton ? 'pr-12' : ''} ${
            error ? 'border-symbiote-red ring-1 ring-symbiote-red' : ''
          }`} 
        />
        {actionButton && (
          <div className="absolute right-2 flex items-center">
            {actionButton}
          </div>
        )}
      </div>
      {/* Mensaje de error condicional */}
      {error && (
        <span className="text-xs font-bold text-symbiote-red mt-1">{error}</span>
      )}
    </div>
  );
}