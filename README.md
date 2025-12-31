# 🤖 AI Chatbot API - LLM-Powered Backend

[![Python](https://img.shields.io/badge/Python-3.12-blue?style=flat-square&logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115%2B-green?style=flat-square&logo=fastapi)](https://fastapi.tiangolo.com)
[![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-336791?style=flat-square&logo=postgresql)](https://postgresql.org)
[![Docker](https://img.shields.io/badge/Docker-Compose-2496ED?style=flat-square&logo=docker)](https://docker.com)
[![Groq](https://img.shields.io/badge/AI-Groq%20Llama%203.3-orange?style=flat-square)](https://groq.com)
[![Tests](https://img.shields.io/badge/Tests-pytest-critical?style=flat-square)](https://pytest.org)
[![License](https://img.shields.io/badge/License-MIT-black?style=flat-square)](LICENSE)

Una **API backend profesional y escalable** para chatbots inteligentes con integración de LLM. Demuestra arquitectura limpia, persistencia de datos, testing automatizado y deployment containerizado.

---

## 📋 Contenido

- [Características](#características)
- [Tech Stack](#tech-stack)
- [Inicio Rápido](#inicio-rápido)
- [Uso de la API](#uso-de-la-api)
- [Estructura del Proyecto](#estructura-del-proyecto)
- [Arquitectura & Decisiones de Diseño](#arquitectura--decisiones-de-diseño)
- [Testing](#testing)
- [Desarrollo Local](#desarrollo-local)
- [Deployment](#deployment)
- [Contribuir](#contribuir)

---

## ✨ Características

### 🐳 Fully Dockerized
- Despliegue completo de API + Base de Datos con un solo comando
- `docker-compose.yml` con healthchecks y configuración lista para producción
- Reproducible en cualquier máquina (Windows, Mac, Linux)

### 🧠 Memoria Persistente
- Historial de conversaciones almacenado en PostgreSQL
- Relaciones 1-N entre Conversaciones y Mensajes
- Recuperación automática del contexto de chat anterior

### ⚡ IA en Tiempo Real
- Integración con Groq API (Llama 3.3 70B - gratuita)
- Soporte para streaming (Server-Sent Events) para baja latencia
- Respuestas en <100ms (excl. inferencia de LLM)

### 🛡️ Production-Ready Code
- **FastAPI + Pydantic V2**: Validación estricta de input/output
- **SQLAlchemy 2.0 Async**: ORM asíncrono sin bloqueos
- **pytest + Mock**: Testing unitario e integración con >80% coverage
- **Type Hints**: 100% type coverage en todo el código
- **Error Handling**: Excepciones personalizadas y global exception handler

---

## 🛠️ Tech Stack

| Componente | Tecnología | Versión | Propósito |
|-----------|-----------|---------|----------|
| **Framework Web** | FastAPI | 0.115+ | API REST asíncrona |
| **Server** | Uvicorn | 0.32+ | Servidor ASGI |
| **Validation** | Pydantic | 2.5+ | Validación de datos |
| **ORM** | SQLAlchemy | 2.0+ | Acceso a base de datos async |
| **Database Driver** | asyncpg | 0.29+ | Driver PostgreSQL async |
| **LLM Provider** | Groq | 0.13+ | API de modelos de lenguaje |
| **Testing** | pytest | 8.0+ | Tests unitarios e integración |
| **Async Testing** | pytest-asyncio | 0.23+ | Soporte para tests async |
| **HTTP Client** | httpx | 0.27+ | Cliente HTTP asíncrono |
| **Container** | Docker | Latest | Containerización |
| **Env Vars** | python-dotenv | 1.0+ | Gestión de configuración |

---

## 🚀 Inicio Rápido

### Requisitos Previos
- **Docker & Docker Compose** instalados ([Descargar](https://docker.com/products/docker-desktop))
- **Groq API Key** (gratis en [console.groq.com](https://console.groq.com/keys))
- **Git** para clonar el repositorio

### Pasos de Instalación

#### 1. Clonar el Repositorio
```bash
git clone https://github.com/felipegiraldi/ai-chatbot-api.git
cd ai-chatbot-api
```

#### 2. Configurar Variables de Entorno
Crea un archivo `.env` en la raíz del proyecto:

```env
# .env
PROJECT_NAME="AI Chatbot API"
GROQ_API_KEY=gsk_tu_api_key_aqui_...
# DATABASE_URL se configura automáticamente en docker-compose
```

**Obtener tu Groq API Key:**
1. Ve a [console.groq.com](https://console.groq.com/keys)
2. Sign up (es gratis)
3. Crea una nueva API key
4. Cópiala en `.env`

#### 3. Iniciar con Docker Compose
```bash
# Construir y levantar servicios
docker-compose up --build

# Primera vez tardará ~30-60 segundos mientras se descargan imágenes
```

**Esperado:**
```
db-1  | database system is ready to accept connections
web-1 | Tablas creadas exitosamente.
web-1 | Uvicorn running on http://0.0.0.0:8000
```

#### 4. Verificar que Todo Funciona
Abre tu navegador en:
- **Swagger UI (Interactive Docs)**: [http://localhost:8000/docs](http://localhost:8000/docs) ← Prueba endpoints aquí
- **ReDoc (Alternative Docs)**: [http://localhost:8000/redoc](http://localhost:8000/redoc)
- **API Health Check**: [http://localhost:8000/health](http://localhost:8000/health)

---

## 📡 Uso de la API

### Flujo Básico de Chatbot

#### Paso 1: Crear una Conversación
```bash
curl -X POST "http://localhost:8000/api/v1/conversations" \
  -H "Content-Type: application/json"
```

**Respuesta:**
```json
{
  "id": 1,
  "created_at": "2025-12-31T13:30:00"
}
```

#### Paso 2: Enviar un Mensaje (Con Historial Automático)
```bash
curl -X POST "http://localhost:8000/api/v1/conversations/1/messages" \
  -H "Content-Type: application/json" \
  -d '{"message": "Hola, soy Felipe, desarrollador Python en Santiago"}'
```

**Respuesta:**
```json
{
  "response": "Hola Felipe! Es un placer conocer a un desarrollador Python en Santiago...",
  "model_used": "llama-3.3-70b-versatile"
}
```

#### Paso 3: El Chatbot Recuerda el Contexto
```bash
curl -X POST "http://localhost:8000/api/v1/conversations/1/messages" \
  -H "Content-Type: application/json" \
  -d '{"message": "¿De dónde soy y qué hago profesionalmente?"}'
```

**Respuesta:**
```json
{
  "response": "Eres de Santiago y eres desarrollador Python. Tu enfoque es en arquitectura de sistemas...",
  "model_used": "llama-3.3-70b-versatile"
}
```

✨ **¡La API recuperó automáticamente el mensaje anterior de la BD!**

### Usando Swagger UI (Recomendado para Testing)
1. Abre [http://localhost:8000/docs](http://localhost:8000/docs)
2. Expande los endpoints `/api/v1/conversations`
3. Haz click en "Try it out"
4. Completa los parámetros
5. Click en "Execute"

---

## 📂 Estructura del Proyecto

```
ai-chatbot-api/
│
├── app/                           # Código principal de la aplicación
│   ├── __init__.py
│   ├── main.py                    # Entry point, configuración FastAPI
│   │
│   ├── api/                       # Capa de transporte (Endpoints/Routers)
│   │   ├── v1/
│   │   │   └── endpoints/
│   │   │       ├── __init__.py
│   │   │       └── chat.py        # POST /conversations, POST /conversations/{id}/messages
│   │   └── deps.py                # Inyección de dependencias
│   │
│   ├── core/                      # Configuración y setup global
│   │   ├── config.py              # Pydantic Settings (env vars)
│   │   ├── exceptions.py          # Custom exceptions (LLMProviderError)
│   │   ├── database.py            # SQLAlchemy engine, AsyncSession, get_db
│   │   └── init_db.py             # Script para crear tablas
│   │
│   ├── models/                    # Modelos de datos
│   │   ├── chat.py                # Pydantic schemas (ChatRequest, ChatResponse)
│   │   ├── error.py               # Error schemas
│   │   └── sql_models.py          # SQLAlchemy ORM models (Conversation, Message)
│   │
│   └── services/                  # Lógica de negocio
│       ├── llm_service.py         # Integración con Groq API, generate_response, stream_response
│       ├── chat_service.py        # Orquestación: guardar msgs, llamar LLM, recuperar historia
│       └── prompt_manager.py      # Gestión centralizada de prompts
│
├── tests/                         # Testing automatizado
│   ├── __init__.py
│   ├── conftest.py                # Fixtures globales (async_client)
│   ├── unit/
│   │   ├── __init__.py
│   │   └── test_logic.py          # Tests de PromptManager
│   └── integration/
│       ├── __init__.py
│       └── test_api.py            # Tests de endpoints (con mocks)
│
├── Dockerfile                     # Imagen Docker de la aplicación
├── docker-compose.yml             # Orquestación de servicios (API + PostgreSQL)
│
├── requirements.txt               # Dependencias de producción
├── requirements-dev.txt           # Dependencias de desarrollo (pytest, mocks)
│
├── .env.example                   # Template de variables de entorno
├── .gitignore
├── README.md                      # Este archivo
└── LICENSE
```

---

## 🏗️ Arquitectura & Decisiones de Diseño

### 1. **Arquitectura Hexagonal (Puertos y Adaptadores)**

```
┌─────────────────────────────────────────┐
│         FastAPI (Adaptador HTTP)        │
│      (/api/v1/conversations, etc)       │
└──────────────┬──────────────────────────┘
               │
┌──────────────▼──────────────────────────┐
│      ChatService (Dominio/Lógica)       │
│  - Crear conversación                   │
│  - Procesar mensaje                     │
│  - Recuperar historial                  │
└──────────────┬──────────────────────────┘
               │
      ┌────────┴────────┐
      │                 │
   ┌──▼──┐        ┌──────▼────┐
   │ LLM │        │ Database  │
   │(API)│        │(PostgreSQL)
   └─────┘        └───────────┘
```

**Por qué:** Separación clara entre API (presentación), dominio (lógica) e infraestructura (DB, LLM). Facilita testing, cambios y escalado.

### 2. **Inyección de Dependencias (FastAPI Depends)**

```python
@router.post("/conversations/{conversation_id}/messages")
async def send_message(
    request: UserMessageRequest,
    conversation_id: int = Path(...),
    db: AsyncSession = Depends(get_db),  # ← Inyectada automáticamente
    service: ChatService = Depends(lambda: ChatService(...))
):
```

**Por qué:** 
- Facilita mocking en tests (no necesita cambiar código del router)
- Loose coupling entre componentes
- Testing sin tocar la lógica real

### 3. **Async/Await en Todo**

Todo es **asíncrono**: requests HTTP, acceso a BD, llamadas a LLM. No hay bloqueos.

```python
async def process_user_message(self, conversation_id: int, user_message: str) -> ChatResponse:
    # Corre en paralelo, no bloquea el servidor
    history = await self.get_conversation_history(conversation_id)
    response = await self.llm.generate_response(user_message, history)
```

**Por qué:** Un servidor FastAPI con 10 workers puede manejar 1000+ requests concurrentes.

### 4. **Separación de Prompts (PromptManager)**

Los prompts **no están hardcodeados** en la lógica:

```python
class PromptManager:
    SYSTEM_PROMPT_TEMPLATE = "Eres un asistente..."
    
    @staticmethod
    def build_messages(user_message: str, history: List[Dict] = None):
        # Centraliza toda lógica de prompts
```

**Por qué:** Los prompts cambian más frecuentemente que el código. Esto permite iterar sin riesgo de romper la lógica.

### 5. **Type Safety con Pydantic V2**

```python
class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, max_length=10000)
    
class ChatResponse(BaseModel):
    response: str
    model_used: str
```

**Por qué:** Validación automática, documentación automática, previene bugs sutiles.

### 6. **Persistencia Asíncrona con SQLAlchemy**

```python
class Conversation(Base):
    __tablename__ = "conversations"
    id: Mapped[int] = mapped_column(primary_key=True)
    messages: Mapped[List["Message"]] = relationship(cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"
    conversation_id: Mapped[int] = mapped_column(ForeignKey("conversations.id"))
```

**Por qué:** 
- Async ORM (no bloquea)
- Type hints con Mapped
- Relaciones automáticas
- Migrations con Alembic (futuro)

---

## 🧪 Testing

### Ejecutar Tests

```bash
# Dentro del contenedor
docker-compose exec web pytest -v

# O localmente (si tienes venv)
pytest tests/ -v --cov=app --cov-report=html
```

### Cobertura

```bash
pytest tests/ --cov=app --cov-report=term-missing
```

**Expected:** >80% coverage en `app/` (excluyendo main.py y init_db.py)

### Tipos de Tests

#### Unit Tests (`tests/unit/test_logic.py`)
```python
def test_build_messages_structure():
    messages = PromptManager.build_messages("Hola")
    assert len(messages) == 2
    assert messages[0]["role"] == "system"
```
Prueban **lógica pura** sin dependencias externas.

#### Integration Tests (`tests/integration/test_api.py`)
```python
@pytest.mark.asyncio
async def test_chat_endpoint_standard(async_client):
    response = await async_client.post("/api/v1/conversations/1/messages", 
                                       json={"message": "Hola"})
    assert response.status_code == 200
```
Prueban **endpoints completos** con **mocks de LLMService** (no consume API quota real).

---

## 💻 Desarrollo Local (Sin Docker)

Para desarrollar sin contenedores:

### 1. Setup del Entorno
```bash
# Crear virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Instalar dependencias
pip install -r requirements.txt
pip install -r requirements-dev.txt  # Para tests
```

### 2. Levantar PostgreSQL (Con Docker solo para DB)
```bash
docker run --name chatbot-db \
  -e POSTGRES_USER=postgres \
  -e POSTGRES_PASSWORD=password \
  -e POSTGRES_DB=chatbot_db \
  -p 5432:5432 \
  -d postgres:16
```

### 3. Configurar Variables de Entorno
```env
PROJECT_NAME=AI Chatbot API
GROQ_API_KEY=gsk_...
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/chatbot_db
```

### 4. Inicializar Base de Datos
```bash
python -m app.core.init_db
# Output: "Tablas creadas exitosamente."
```

### 5. Correr Servidor
```bash
uvicorn app.main:app --reload
```
Ahora puedes editar código y ver cambios en tiempo real.

### 6. Correr Tests
```bash
pytest tests/ -v
```

---

## 🚢 Deployment

### Opción 1: Railway (Recomendado para MVP)

1. **Sign up** en [railway.app](https://railway.app)
2. **Conectar tu GitHub** (fork/push este repo)
3. **Crear proyectos:**
   - PostgreSQL (agregar de marketplace)
   - Python Web Service (from GitHub repo)
4. **Set Environment Variables:**
   - `GROQ_API_KEY=gsk_...`
   - `DATABASE_URL=postgresql://...` (Railway la genera automáticamente)
5. **Deploy** (automático en cada push)

### Opción 2: Docker Swarm / Kubernetes

Para producción de mayor escala, construye la imagen y despliégala:

```bash
docker build -t ai-chatbot-api:latest .
docker tag ai-chatbot-api:latest your-registry/ai-chatbot-api:latest
docker push your-registry/ai-chatbot-api:latest
```

Luego configura en tu K8s/Docker Swarm.

### Opción 3: AWS ECS / Google Cloud Run

Las imágenes Docker se pueden desplegar directamente en cualquier servicio de contenedores.

---

## 📊 Performance & Monitoreo

### Métricas Esperadas

| Métrica | Valor | Nota |
|---------|-------|------|
| **Latencia API** | <100ms | Excl. inferencia LLM |
| **Latencia LLM** | 2-5s | Dependiendo del modelo |
| **Throughput** | 100+ req/s | Con 10 workers Uvicorn |
| **Memoria** | ~500MB | API + connpool DB |
| **Test Coverage** | >80% | Del código en `app/` |

### Monitoring Futuro

Para monitoreo avanzado, agrega:
- **Prometheus** para métricas
- **Grafana** para dashboards
- **Jaeger** para tracing distribuido
- **DataDog** o **New Relic** para APM

---


## 📜 Licencia

MIT © 2025 Felipe Giraldi

---

## 🔗 Links Útiles

- **Groq Console:** https://console.groq.com
- **FastAPI Docs:** https://fastapi.tiangolo.com
- **SQLAlchemy Async:** https://docs.sqlalchemy.org/en/20/orm/extensions/asyncio.html
- **Docker Compose:** https://docs.docker.com/compose
- **pytest:** https://docs.pytest.org

---

## ✋ Soporte

Preguntas o issues? 

- 📧 Email: felipegiraldiv@gmail.com
- 🔗 LinkedIn: https://linkedin.com/in/felipe-giraldi-1a8264314
- 💬 Abre un [Issue en GitHub](https://github.com/felipegiraldi/ai-chatbot-api/issues)

---

**Built by Felipe Giraldi** | Santiago, Chile 🇨🇱

