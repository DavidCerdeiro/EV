# 🕷️ Asistente E.V.

![Status: Phase 23](https://img.shields.io/badge/Status-Phase_3_Completed-brightgreen)
![React](https://img.shields.io/badge/Frontend-React_+_Vite-blue)
![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688)
![Docker](https://img.shields.io/badge/Infra-Docker-2496ED)
![PostgreSQL](https://img.shields.io/badge/DB-PostgreSQL_pgvector-336791)

[🇪🇸 Español](#-español) | [🇬🇧 English](#-english)

---

## 🇪🇸 Español

E.V. (inspirado en la asistente de Spiderman en la película Brand New Day) es una aplicación web donde interactúas con un agente de IA mediante voz. Este repositorio contiene la arquitectura completa del proyecto estructurada en microservicios locales.

### 🚀 Estado Actual
El proyecto acaba de completar la **Fase 3: Integración de Sentidos**. El usuario puede hablar con la asistente y esta le contestará. 

### 💻 Tecnologías Core
*   **Frontend:** React con Vite.
*   **Backend:** FastAPI (Python).
*   **Base de Datos:** PostgreSQL con la extensión pgvector.
*   **Orquestación:** Docker Compose.
*   **IA & Agentes:** LangChain, Groq (GPT OSS (120B y 20B)).

### 🛠️ Instalación y Uso

1.  **Requisitos previos:** Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2.  **Configurar Variables de Entorno:** Crea tu archivo local de configuración a partir de la plantilla:
    ```bash
    cp .env.example .env
    ```
    *Abre el archivo `.env` y rellena tus credenciales (ver sección "Configuración de Credenciales" más abajo).*
3.  **Levantar servicios::**
    ```bash
    docker-compose up -d --build
    ```
4.  **Accesos y Certificado Local SSL:**
    *   Interfaz Gráfica (UI): `http://localhost:3000`. ⚠️ Importante: Ve a esta URL primero. Tu navegador mostrará una alerta de "Conexión no privada". Esto es normal porque usamos un certificado local (vía Caddy) necesario para las integraciones de OAuth 2.0. Haz clic en Configuración avanzada > Continuar a localhost.
    *   Documentación API (Swagger): `http://localhost:8000/docs`.

### 🎨 Diseño y Accesibilidad (UX/UI)
*   **Contraste Simbionte:** Diseño agresivo y minimalista en *Dark Mode* extremo (negro puro y detalles en rojo intenso), inspirado en la paleta de Venom y Miles Morales.
*   **Accesibilidad:** Integración de atributos `aria-live="polite"` para lectores de pantalla, navegación nativa por teclado y alertas visuales (animaciones CSS como *pulse*) para usuarios con daltonismo.
*   **Control de Voz:** Incorpora mecánicas de interrupción (botón Stop) y confirmación de transcripción exacta antes de procesar el input.

### 🗺️ Roadmap (Fases del Proyecto)

*   [x] **Fase 1: Arquitectura Base.** Contenedores Docker, FastAPI, PostgreSQL (pgvector) y UI en React.
*   [x] **Fase 2: Orquestación de IA.** Endpoints REST en FastAPI e integración de LangChain con Groq.
*   [x] **Fase 3: Integración de Sentidos.** Transcripción y síntesis de voz en el cliente usando Web Speech API nativa en React.
*   [ ] **Fase 4: Function Calling.** Integración local segura mediante `.env` con Google Calendar, Drive, Gmail, GitHub, Spotify y Weather API.
*   [ ] **Fase 5: Persistencia.** Memoria semántica relacional y búsqueda vectorial para módulo de notas usando pgvector.

---

## 🇬🇧 English

E.V. (inspired by Spider-Man's assistant in the Brand New Day storyline) is a web application where you interact with an AI agent acting as your personal assistant via voice commands. This repository contains the full project architecture built on local microservice.

### 🚀 Current Status
The project has just completed **Phase 3: Sensory Integration**. The user can talk with the agent and it will respond. 

### 💻 Core Technologies
*   **Frontend:** React with Vite.
*   **Backend:** FastAPI (Python).
*   **Database:** PostgreSQL with the pgvector extension.
*   **Orchestration:** Docker Compose.
*   **AI & Agents:** LangChain, Groq (GPT OSS (120B and 20B)).

### 🛠️ Getting Started (Phase 1)

1.  **Prerequisites:** Make sure you have Docker and Docker Compose installed on your system.
2.  **Clone and run services:**
    ```bash
    git clone [https://github.com/your-username/asistente-ev.git](https://github.com/your-username/asistente-ev.git)
    cd asistente-ev
    docker-compose up -d
    ```
    *This command orchestrates three services: frontend, backend, and database on the same network*.
3.  **Access Points:**
    *   Graphical Interface (UI): `http://localhost:3000`.
    *   API Documentation (Swagger): `http://localhost:8000/docs`.

### 🎨 Design & Accessibility (UX/UI)
*   **Symbiote Contrast:** An aggressive, minimalist extreme Dark Mode (pure black backgrounds with vivid red accents), inspired by Venom and Miles Morales.
*   **Accessibility:** Includes `aria-live="polite"` wrappers for screen readers, native keyboard navigation via `<button>` tags, and color-independent status indicators (e.g., CSS pulse animations) for colorblind users.
*   **Voice Control:** Features interrupt mechanics (Stop button for long outputs) and exact transcription confirmation before the AI begins processing.

### 🗺️ Roadmap (Project Phases)

*   [x] **Phase 1: Base Architecture.** Docker containers, FastAPI, PostgreSQL (pgvector), and React UI.
*   [x] **Phase 2: AI Orchestration.** FastAPI REST endpoints and LangChain integration with Groq.
*   [x] **Phase 3: Sensory Integration.** Client-side voice transcription and synthesis using the native Web Speech API in React.
*   [ ] **Phase 4: Function Calling.** Secure local integrations (via `.env`) with Google Calendar, Drive, Gmail, GitHub, Spotify, and Weather API.
*   [ ] **Phase 5: Persistence.** Relational semantic memory and vector search for the notes module using pgvector.
