import { useState, useEffect } from 'react';
import { ConfigurationButton } from '../components/ConfigurationButton/ConfigurationButton';
import { InputBox } from '../components/InputBox/InputBox';
import { GeoPermissionModal } from '../components/GeoPermissionModal/GeoPermissionModal';

export function RightSidebar({ 
  isConfigOpen, 
  onConfigToggle 
}: { 
  isConfigOpen: boolean; 
  onConfigToggle: () => void 
}) {
  const [name, setName] = useState('');
  const [location, setLocation] = useState('');
  
  const [isGeoModalOpen, setIsGeoModalOpen] = useState(false);
  const [isLocating, setIsLocating] = useState(false);
  
  // Nuevos estados para validación al guardar
  const [isSaving, setIsSaving] = useState(false);
  const [locationError, setLocationError] = useState('');

  useEffect(() => {
    const savedName = localStorage.getItem('ev_userName') || '';
    const savedLocation = localStorage.getItem('ev_userLocation') || '';
    setName(savedName);
    setLocation(savedLocation);
  }, [isConfigOpen]); // Recargar al abrir por si se borraron externamente

  useEffect(() => {
    const handleKeyDown = (e: KeyboardEvent) => {
      if (e.key === 'Escape') {
        if (isGeoModalOpen) setIsGeoModalOpen(false);
        else if (isConfigOpen && !isSaving) onConfigToggle();
      }
    };
    window.addEventListener('keydown', handleKeyDown);
    return () => window.removeEventListener('keydown', handleKeyDown);
  }, [isConfigOpen, isGeoModalOpen, isSaving, onConfigToggle]);

  const handleSave = async () => {
    setLocationError('');
    const trimmedLocation = location.trim();

    // Si está vacío, limpiamos datos y guardamos (Opcional: podrías querer enviar esto al backend también para borrarlo allí)
    if (!trimmedLocation) {
      localStorage.setItem('ev_userName', name);
      localStorage.setItem('ev_userLocation', '');
      onConfigToggle();
      return;
    }

    setIsSaving(true);

    try {
      // Validate location using OpenStreetMap Nominatim API
      const responseGeo = await fetch(
        `https://nominatim.openstreetmap.org/search?q=${encodeURIComponent(trimmedLocation)}&format=json&limit=1&accept-language=es`
      );
      const dataGeo = await responseGeo.json();

      if (dataGeo && dataGeo.length > 0) {
        const validCity = dataGeo[0].name;

        const userData = {
          name: name,
          city_name: validCity,
        };
        
        const responseBackend = await fetch('http://127.0.0.1:8000/user/', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify(userData),
        });

        if (!responseBackend.ok) {
          throw new Error(`Error HTTP: ${responseBackend.status}`);
        }

        // If everything is successful, save to localStorage and update state
        localStorage.setItem('ev_userName', name);
        localStorage.setItem('ev_userLocation', validCity);
        setLocation(validCity); 

        onConfigToggle(); // Close the configuration panel after saving
      } else {
        setLocationError('No se ha encontrado esta ubicación. Intenta ser más específico.');
      }
    } catch (error) {
      console.error("Error al guardar:", error);
      setLocationError('Error de conexión al validar o guardar la ubicación.');
    } finally {
      setIsSaving(false);
    }
  };

  const handleDetectLocation = () => {
    setIsLocating(true);
    setLocationError(''); // Limpiamos errores previos si los hubiera
    
    if (!navigator.geolocation) {
      alert("Tu navegador no soporta geolocalización.");
      setIsLocating(false);
      setIsGeoModalOpen(false);
      return;
    }

    navigator.geolocation.getCurrentPosition(
      async (position) => {
        const { latitude, longitude } = position.coords;
        try {
          const response = await fetch(
            `https://nominatim.openstreetmap.org/reverse?format=json&lat=${latitude}&lon=${longitude}&accept-language=es`
          );
          const data = await response.json();
          const city = data.address.city || data.address.town || data.address.village || data.address.county;
          if (city) {
            setLocation(city);
          }
        } catch (error) {
          console.error("Error al obtener la ciudad:", error);
        } finally {
          setIsLocating(false);
          setIsGeoModalOpen(false);
        }
      },
      (error) => {
        console.error("Error de geolocalización:", error);
        setIsLocating(false);
        setIsGeoModalOpen(false);
      }
    );
  };

  return (
    <aside className="ev-sidebar-right relative">
      <ConfigurationButton 
        onClick={onConfigToggle} 
        aria-expanded={isConfigOpen}
        aria-controls="ev-config-sidebar"
        aria-label="Abrir menú de configuración"
      />

      {isConfigOpen && (
        <div 
          className="ev-config-overlay"
          onClick={() => {
            if (!isGeoModalOpen && !isSaving) onConfigToggle();
          }}
          aria-hidden="true"
        />
      )}

      <div 
        id="ev-config-sidebar"
        role="dialog"
        aria-modal="true"
        aria-labelledby="ev-config-title"
        className={`ev-config-panel ${isConfigOpen ? 'translate-x-0' : 'translate-x-full'}`}
      >
        <div className="ev-config-header">
          <h2 id="ev-config-title" className="ev-config-title">Configuración</h2>
          <button 
            onClick={onConfigToggle} 
            className="ev-config-close-btn disabled:opacity-50"
            aria-label="Cerrar configuración"
            title="Cerrar"
            disabled={isSaving}
          >
            <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
              <line x1="18" y1="6" x2="6" y2="18"></line>
              <line x1="6" y1="6" x2="18" y2="18"></line>
            </svg>
          </button>
        </div>
        
        <div className="ev-config-form">
          <InputBox 
            id="userName" 
            labelText="Nombre" 
            placeholder="Ej. David" 
            value={name}
            onChange={(e) => setName(e.target.value)}
            autoFocus={isConfigOpen} 
          />
          <InputBox 
            id="userLocation" 
            labelText="Localidad" 
            placeholder="Ej. Cádiz" 
            value={location}
            onChange={(e) => {
              setLocation(e.target.value);
              if (locationError) setLocationError(''); // Limpia el error al volver a escribir
            }}
            error={locationError}
            actionButton={
              <button
                onClick={() => setIsGeoModalOpen(true)}
                className="ev-icon-btn"
                title="Detectar ubicación actual"
                aria-label="Detectar ubicación actual"
                disabled={isSaving}
              >
                {isLocating ? (
                  <svg className="animate-spin h-5 w-5 text-symbiote-red" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                    <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                    <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
                  </svg>
                ) : (
                  <svg xmlns="http://www.w3.org/2000/svg" width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
                    <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z"></path>
                    <circle cx="12" cy="10" r="3"></circle>
                  </svg>
                )}
              </button>
            }
          />
        </div>

        <div className="ev-config-footer">
          <button 
            type="button"
            className="ev-btn-primary disabled:opacity-50 disabled:cursor-not-allowed flex justify-center items-center"
            onClick={handleSave}
            aria-label="Guardar configuración"
            disabled={isSaving}
          >
            {isSaving ? (
              <svg className="animate-spin h-5 w-5 text-symbiote-red mr-2" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
                <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
                <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
              </svg>
            ) : null}
            {isSaving ? 'Validando...' : 'Guardar'}
          </button>
        </div>
      </div>

      <GeoPermissionModal 
        isOpen={isGeoModalOpen}
        isLocating={isLocating}
        onClose={() => setIsGeoModalOpen(false)}
        onConfirm={handleDetectLocation}
      />
    </aside>
  );
}