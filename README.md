# 🕷️ Asistente E.V.

![Status: Phase 3](https://img.shields.io/badge/Status-Phase_3_Completed-brightgreen)
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
-   **Frontend:** React con Vite.
-   **Backend:** FastAPI (Python).
-   **Base de Datos:** PostgreSQL con la extensión pgvector.
-   **Orquestación:** Docker Compose.
-   **IA & Agentes:** LangChain, Groq (GPT OSS (120B y 20B)).

### 🛠️ Instalación y Uso

1.  **Requisitos previos:** Asegúrate de tener Docker y Docker Compose instalados en tu sistema.
2.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/asistente-ev.git
    cd asistente-ev
    ```
3.  **Configurar Variables de Entorno:**
    Crea tu archivo local de configuración a partir de la plantilla:
    ```bash
    cp .env.example .env
    ```
    *Abre el archivo `.env` y rellena tus credenciales (ver sección "Configuración de Credenciales" más abajo).*
4.  **Levantar servicios:**
    ```bash
    docker-compose up -d --build
    ```
5.  **Accesos:**
    *   **Backend (Swagger):** `http://127.0.0.1:8000/docs`. 
    *   **Interfaz Gráfica (UI):** `http://127.0.0.1:3000`.

### 🔑 Configuración de Credenciales (Fase 4)
Para que E.V. pueda acceder a tus servicios, necesitas rellenar el archivo `.env` con tus propias credenciales. Las **URL de redirección (Callback URI)** para los servicios OAuth deben configurarse estrictamente como: `http://127.0.0.1:8000/callback` (o la ruta específica que definas en FastAPI, como `/auth/google/callback`).

-   **Google Workspace (Calendar / Gmail):**
    1. Ve a [Google Cloud Console](https://console.cloud.google.com/), crea un proyecto y habilita "Google Calendar API" y "Gmail API".
    2. Configura la "Pantalla de consentimiento de OAuth" (añade tu propio correo como usuario de prueba).
    3. En "Credenciales", crea un **ID de cliente de OAuth** (Tipo: *Aplicación web*).
    4. Añade `http://127.0.0.1:8000/callback` en "URI de redireccionamiento autorizados". Copia el *Client ID* y *Client Secret*.
-   **Google Weather API:**
    1. En el mismo proyecto de [Google Cloud Console](https://console.cloud.google.com/), habilita la "Weather API".
    2. Ve a **Credenciales > Crear credenciales > Clave de API**.
    3. Copia la clave generada y pégala como `GOOGLE_WEATHER_API_KEY` en tu `.env`.
-   **Spotify:**
    1. Ve a [Spotify for Developers](https://developer.spotify.com/dashboard) y crea una app.
    2. En *Redirect URIs*, añade `http://127.0.0.1:8000/callback` y pulsa "Add" y luego "Save". Copia el *Client ID* y *Client Secret*.
-   **GitHub:**
    1. Ve a [GitHub Developer Settings > Personal access tokens > Fine-grained tokens](https://github.com/settings/apps).
    2. Genera un token nuevo con permisos para leer tus repositorios/issues. Pega el token (empieza por `github_pat_`) directamente como API Key en tu `.env`.
-   **Groq (LLM):**
    Crea una cuenta en [Groq Console](https://console.groq.com/) y genera una API Key para habilitar la inteligencia del asistente.

### 🎨 Diseño y Accesibilidad (UX/UI)
-   **Contraste Simbionte:** Diseño agresivo y minimalista en *Dark Mode* extremo (negro puro y detalles en rojo intenso), inspirado en la paleta de Venom y Miles Morales.
-   **Accesibilidad:** Integración de atributos `aria-live="polite"` para lectores de pantalla, navegación nativa por teclado y alertas visuales (animaciones CSS como *pulse*) para usuarios con daltonismo.
-   **Control de Voz:** Incorpora mecánicas de interrupción (botón Stop) y confirmación de transcripción exacta antes de procesar el input.

### 🗺️ Roadmap (Fases del Proyecto)

-   [x] **Fase 1: Arquitectura Base.** Contenedores Docker, FastAPI, PostgreSQL (pgvector) y UI en React.
-   [x] **Fase 2: Orquestación de IA.** Endpoints REST en FastAPI e integración de LangChain con Groq.
-   [x] **Fase 3: Integración de Sentidos.** Transcripción y síntesis de voz en el cliente usando Web Speech API nativa en React.
-   [ ] **Fase 4: Function Calling.** Integración local segura mediante `.env` con Google Calendar, Drive, Gmail, GitHub, Spotify y Weather API.
-   [ ] **Fase 5: Persistencia.** Memoria semántica relacional y búsqueda vectorial para módulo de notas usando pgvector.

---

## 🇬🇧 English

E.V. (inspired by Spider-Man's assistant in the Brand New Day storyline) is a web application where you interact with an AI agent acting as your personal assistant via voice commands. This repository contains the full project architecture built on local microservices.

### 🚀 Current Status
The project has just completed **Phase 3: Sensory Integration**. The user can talk with the agent and it will respond. 

### 💻 Core Technologies
-   **Frontend:** React with Vite.
-   **Backend:** FastAPI (Python).
-   **Database:** PostgreSQL with the pgvector extension.
-   **Orchestration:** Docker Compose.
-   **AI & Agents:** LangChain, Groq (GPT OSS (120B and 20B)).

### 🛠️ Getting Started

1.  **Prerequisites:** Make sure you have Docker and Docker Compose installed on your system.
2.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-username/asistente-ev.git
    cd asistente-ev
    ```
3.  **Environment Variables:**
    Create your local configuration file from the template:
    ```bash
    cp .env.example .env
    ```
    *Open the `.env` file and fill in your credentials (see the "Credentials Setup" section below).*
4.  **Run services:**
    ```bash
    docker-compose up -d --build
    ```
5.  **Access Points:**
    *   **Backend (Swagger):** `http://127.0.0.1:8000/docs`. 
    *   **Graphical Interface (UI):** `http://127.0.0.1:3000`.

### 🔑 Credentials Setup (Phase 4)
For E.V. to access your services, you must fill the `.env` file with your own credentials. The **Redirect URIs (Callback URI)** for OAuth services must be strictly set to: `http://127.0.0.1:8000/callback` (or the specific route you define in FastAPI, such as `/auth/google/callback`).

-   **Google Workspace (Calendar / Gmail):**
    1. Go to [Google Cloud Console](https://console.cloud.google.com/), create a project, and enable "Google Calendar API" and "Gmail API".
    2. Configure the "OAuth consent screen" (add your email as a test user).
    3. Under "Credentials", create an **OAuth client ID** (Type: *Web application*).
    4. Add `http://127.0.0.1:8000/callback` under "Authorized redirect URIs". Copy the *Client ID* and *Client Secret*.
-   **Google Weather API:**
    1. In the same [Google Cloud Console](https://console.cloud.google.com/) project, enable the "Weather API".
    2. Go to **Credentials > Create credentials > API key**.
    3. Copy the generated key and paste it as `GOOGLE_WEATHER_API_KEY` in your `.env`.
-   **Spotify:**
    1. Go to [Spotify for Developers](https://developer.spotify.com/dashboard) and create an app.
    2. Under *Redirect URIs*, add `http://127.0.0.1:8000/callback` and click "Add" and then "Save". Copy the *Client ID* and *Client Secret*.
-   **GitHub:**
    1. Go to [GitHub Developer Settings > Personal access tokens > Fine-grained tokens](https://github.com/settings/apps).
    2. Generate a new token with read/write permissions for your repositories/issues. Paste this token (starts with `github_pat_`) directly as an API Key in your `.env`.
-   **Groq (LLM):**
    Create an account at [Groq Console](https://console.groq.com/) and generate an API Key to enable the assistant's core intelligence.

### 🎨 Design & Accessibility (UX/UI)
-   **Symbiote Contrast:** An aggressive, minimalist extreme Dark Mode (pure black backgrounds with vivid red accents), inspired by Venom and Miles Morales.
-   **Accessibility:** Includes `aria-live="polite"` wrappers for screen readers, native keyboard navigation via `<button>` tags, and color-independent status indicators (e.g., CSS pulse animations) for colorblind users.
-   **Voice Control:** Features interrupt mechanics (Stop button for long outputs) and exact transcription confirmation before the AI begins processing.

### 🗺️ Roadmap (Project Phases)

-   [x] **Phase 1: Base Architecture.** Docker containers, FastAPI, PostgreSQL (pgvector), and React UI.
-   [x] **Phase 2: AI Orchestration.** FastAPI REST endpoints and LangChain integration with Groq.
-   [x] **Phase 3: Sensory Integration.** Client-side voice transcription and synthesis using the native Web Speech API in React.
-   [ ] **Phase 4: Function Calling.** Secure local integrations (via `.env`) with Google Calendar, Drive, Gmail, GitHub, Spotify, and Weather API.
-   [ ] **Phase 5: Persistence.** Relational semantic memory and vector search for the notes module using pgvector.