# 🚀 Post GenerAItor: Un Asistente de Contenido con IA y Agentes Especializados

<img width="2079" height="320" alt="Captura de pantalla 2025-07-30 121038" src="https://github.com/user-attachments/assets/3ee032c2-a4fa-4d47-8da3-fab2bc020796" />

**Post GenerAItor** es una aplicación full-stack desarrollada para explorar y demostrar las capacidades de los Grandes Modelos de Lenguaje (LLMs) y los patrones de IA modernos. La aplicación cuenta con múltiples agentes de IA especializados, cada uno diseñado para una tarea específica, desde la creación de contenido creativo hasta la investigación factual basada en documentos.

## ✨ Características Principales de la Aplicación

Este proyecto no es solo un generador de texto; es una suite de herramientas de IA:

*   **Agente de Contenido:**
    *   **Generación Multi-Plataforma:** Crea borradores optimizados para **Blogs**, **X (Twitter)** e **Instagram**.
    *   **Soporte Multi-Idioma:** Genera contenido en 6 idiomas diferentes.
    *   **Agente de Búsqueda Integrado:** Puede realizar búsquedas web en tiempo real a través de **Tavily** para crear contenido sobre eventos actuales o temas financieros.
    *   **Contexto de Marca:** Permite al usuario proporcionar información sobre su empresa para personalizar el tono y el contenido.
    *   **Enriquecimiento Visual:** Acompaña cada generación con una imagen relevante de la API de **Unsplash**.

*   **Agente de RAG Científico:**
    *   **Base de Conocimiento Propia:** Indexa documentos PDF de investigación para crear una base de datos vectorial con **ChromaDB**.
    *   **Respuestas Fundamentadas:** Responde preguntas complejas basándose únicamente en el conocimiento de los documentos indexados.
    *   **Guardarraíl Anti-Alucinaciones:** Incluye una cadena de verificación de IA que actúa como "juez", evaluando si la respuesta es fiel al contexto de los documentos para garantizar la fiabilidad.

*   **Trazabilidad y Observabilidad:**
    *   Integrado con **LangSmith** para una depuración y visualización completa de las cadenas y agentes de IA.

## 🛠️ Stack Tecnológico

Este proyecto fue construido priorizando la velocidad de desarrollo y las herramientas modernas del ecosistema de IA.

*   **Frontend:** React, Vite, TypeScript, Tailwind CSS
*   **Backend:** FastAPI (Python)
*   **LLMs:** Ollama (`llama3`), Google Gemini
*   **Frameworks de IA:** LangChain, LangSmith
*   **Bases de Datos Vectoriales:** ChromaDB
*   **Herramientas de Agente:** Tavily Search API
*   **APIs Externas:** Unsplash API
*   **Contenerización:** Docker, Docker Compose

---

## 🚀 Cómo Empezar.

La forma más fácil y recomendada de ejecutar este proyecto es con Docker. Solo necesitas tener Docker y Docker Compose instalados.

1.  **Clona el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/p-XI-llm-content-generator.git
    cd p-XI-llm-content-generator
    ```

2.  **Configura tus claves de API:**
    Crea un archivo `.env` en la raíz del proyecto y rellenar tus claves:
    ```.env
    # --- API Keys ---
    GOOGLE_API_KEY="AIzaSy..."
    UNSPLASH_ACCESS_KEY="..."
    TAVILY_API_KEY="tvly-..."
    
    # --- Ollama Hosts (para Docker) ---
    OLLAMA_DOCKER_HOST="http://host.docker.internal:11434"
    
    # --- LangSmith Configuration ---
    LANGCHAIN_TRACING_V2="true"
    LANGCHAIN_ENDPOINT="https://api.smith.langchain.com"
    LANGCHAIN_API_KEY="ls__..."
    LANGCHAIN_PROJECT="GenerAItor Sprint"
    ```

3.  **Asegúrate de que Ollama esté corriendo:**
    Este setup asume que tienes [Ollama](https://ollama.com/) instalado y corriendo en tu máquina anfitriona (fuera de Docker). Asegúrate de tener el modelo `llama3` descargado:
    ```bash
    ollama pull llama3
    ```

4.  **Construye y levanta los contenedores:**
    Este comando construirá las imágenes y levantará el frontend y el backend.
    ```bash
    docker-compose up --build
    ```
    La primera vez puede tardar unos minutos.

5.  **Crea la base de conocimiento RAG:**
    En una **nueva terminal**, con los contenedores ya corriendo, ejecuta el script de ingesta de datos dentro del contenedor del backend:
    ```bash
    docker-compose exec backend python server/scripts/ingest_data.py
    ```

6.  **¡Listo!**
    *   Abre tu navegador y ve a `http://localhost:5173`.
    *   Explora las diferentes funcionalidades de los agentes.

---

## 🖼️ Galería (Screenshots).

<img width="1968" height="1040" alt="Captura de pantalla 2025-07-30 121105" src="https://github.com/user-attachments/assets/ffd9a4cd-09eb-4213-8920-a0a613cfa24b" />

<img width="1081" height="1360" alt="Captura de pantalla 2025-07-30 144017" src="https://github.com/user-attachments/assets/4b3df750-fd81-4417-a8b4-3297cc48b4d7" />

<img width="1073" height="1426" alt="Captura de pantalla 2025-07-30 144006" src="https://github.com/user-attachments/assets/56f4d868-09d5-4d3f-8a16-29ef897ef691" />

<img width="1237" height="1619" alt="Captura de pantalla 2025-07-30 150138" src="https://github.com/user-attachments/assets/cf87ecf1-e7f5-41d9-890f-86727575d3dc" />

## 📝 Próximos Pasos (Posibles Mejoras) a desarrollar.

*   **Agente de Consultas Unificado:** Finalizar y estabilizar el `Query Agent` como interfaz principal.
*   **PoC de GraphRAG:** Mejorar la extracción de entidades para hacer el grafo más robusto y útil.
*   **Streaming de Respuestas:** Implementar streaming para que el texto de la IA aparezca palabra por palabra, mejorando la UX.

