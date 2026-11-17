interface GeoPermissionModalProps {
  isOpen: boolean;
  isLocating: boolean;
  onClose: () => void;
  onConfirm: () => void;
}

export function GeoPermissionModal({ 
  isOpen, 
  isLocating, 
  onClose, 
  onConfirm 
}: GeoPermissionModalProps) {
  if (!isOpen) return null;

  return (
    <div className="ev-modal-backdrop">
      <div 
        className="ev-modal-overlay" 
        onClick={() => !isLocating && onClose()}
      />
      <div className="ev-modal-content" role="dialog" aria-labelledby="geo-modal-title">
        <h3 id="geo-modal-title" className="ev-modal-title">Permiso de ubicación</h3>
        <p className="ev-modal-text">
          E.V. necesita acceso a tu ubicación con el objetivo de mejorar las predicciones meteorológicas y ofrecerte información más precisa.
        </p>
        <div className="ev-modal-actions">
          <button 
            onClick={onClose}
            className="ev-btn-secondary"
            disabled={isLocating}
          >
            Cancelar
          </button>
          <button 
            onClick={onConfirm}
            className="ev-btn-danger"
            disabled={isLocating}
          >
            {isLocating ? 'Detectando...' : 'Permitir'}
          </button>
        </div>
      </div>
    </div>
  );
}