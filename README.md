# 🏗️ Architecture Overview

This system is designed as a modular, event‑driven smart home platform.  
Each microservice has a single responsibility and communicates asynchronously via **RabbitMQ**.  
The architecture ensures scalability, strict separation of concerns, and clear data flow from user input to device execution.

---

## 🎙️ STT Service

- **Input:** Audio files (ogg/wav/mp3) from users (voice commands).  
- **Processing:** Speech‑to‑Text conversion using **Whisper** (high accuracy) or **Vosk** (lightweight, offline).  
- **Output:** Plain text representation of the spoken command.  
- **API:**  
  - `POST /stt` → `{ "text": "open the door" }`  
- **Role:** Acts as the audio ingestion layer, enabling voice‑driven control of smart devices.  

**Dependencies:**  

- `openai-whisper` → neural model for speech recognition.  
- `pydub` → audio preprocessing (conversion, slicing, normalization).  
- `faststream[rabbit]` → publish transcription results into RabbitMQ.  
- `dishka` → dependency injection for modular design.  
- `pydantic` → strict DTO validation for transcription results.  
- `uvicorn` → lightweight ASGI server for exposing the API.

---

## 🧠 NLU / RAG Service

- **Input:** Text commands (from STT or directly typed).  
- **Processing:**  
  - Semantic search in **Qdrant/ChromaDB** using embeddings from **SentenceTransformers**.  
  - Generative models (**Gemma / Mistral / Llama**) resolve intent and enrich context.  
- **Output:** Structured command DTO with explicit fields.  
- **API:**  
  - `POST /nlu` → `{ "cmd": "unlock", "device": "front_door", "value": {} }`  
- **Role:** Serves as the intelligence layer, transforming natural language into actionable, machine‑readable commands.  

**Dependencies:**  

- `sentence-transformers` → embedding generation for semantic search.  
- `transformers` + `torch` → inference with generative LLMs.  
- `qdrant-client` → vector database for semantic retrieval.  
- `faststream[rabbit]` → publish structured commands into RabbitMQ.  
- `dishka` → dependency injection for modularity.  
- `pydantic` → DTO validation for parsed commands.  
- `uvicorn` → ASGI runtime for exposing APIs.

---

## 🔐 Command Service (Backend)

- **Responsibilities:**  
  - Validate user permissions (`user_id` → allowed devices).  
  - Normalize and publish commands into **RabbitMQ** using **FastStream**.  
  - Ensure traceability with `request_id`.  
- **API:**  
  - `POST /command` → `{ "ok": true, "request_id": "..." }`  
- **Role:** Central dispatcher that enforces security and routes commands to the execution pipeline.  

**Dependencies:**  

- `faststream[rabbit]` → publish validated commands into RabbitMQ.  
- `dishka` → dependency injection for modular design.  
- `pydantic` → strict DTO validation for commands and permissions.  
- `uvicorn` → ASGI runtime for exposing APIs.

---

## 🤖 Bot Service

- **Responsibilities:**  
  - Handle Telegram messages (text & voice).  
  - Voice → forward to **STT Service**.  
  - Text → forward to **NLU/RAG Service**.  
  - Forward structured result to **Command Service**.  
  - Send execution status/response back to the user.  
- **Role:** Provides conversational interface, bridging end‑users with backend services through Telegram.  

**Dependencies:**  

- `aiogram` → Telegram bot framework for handling updates and commands.  
- `faststream[rabbit]` → publish/consume messages via RabbitMQ.  
- `psycopg` → persist user sessions, permissions, and logs in PostgreSQL.  
- `dishka` → dependency injection for modular design.  

---

## 🌐 WebApp Service

- **Responsibilities:**  
  - Provide a web‑based UI for smart home control.  
  - Send commands directly to **Command Service**.  
  - Display device statuses, logs, and analytics.  
- **Role:** Acts as the presentation layer, enabling browser‑based interaction and monitoring.  

**Dependencies:**  

- `fastapi` → high‑performance HTTP framework for building REST APIs and UI endpoints.  
- `faststream[rabbit]` → integration with RabbitMQ for event‑driven updates.  
- `psycopg` → PostgreSQL persistence for device states, logs, and analytics.  
- `dishka` → dependency injection for modular design.  
- `pydantic` → strict DTO validation for API requests/responses.  
- `uvicorn` → ASGI runtime for serving the web application.

---

## 🔌 Device Gateway

- **Responsibilities:**  
  - Subscribe to **RabbitMQ** for incoming commands.  
  - Execute commands on physical devices via **MQTT** or **HTTP/REST** depending on device capabilities.  
  - Publish execution statuses and telemetry back into the system.  
- **Role:** Hardware integration layer, connecting abstract commands to real‑world device actions.  

**Dependencies:**  

- `gmqtt` → MQTT client for publishing commands and subscribing to device topics.  
- `aiohttp` → HTTP client for devices that expose REST APIs.  
- `faststream[rabbit]` → consume commands from RabbitMQ.  
- `psycopg` → persist device telemetry and execution logs in PostgreSQL.  
- `dishka` → dependency injection for modular design.  
- `pydantic` → DTO validation for commands and statuses.  
- `uvicorn` → ASGI runtime for exposing APIs and health checks.
