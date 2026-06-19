```markdown
# 📻 AudiX Engine: Multimodal Audio Content Localization & Semantic Discovery Pipeline

[![FastAPI](https://img.shields.io/badge/FastAPI-005571?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com)
[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Python 3.10](https://img.shields.io/badge/Python-3.10-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![PyTorch CPU](https://img.shields.io/badge/PyTorch-2.3.0_CPU-EE4C2C?style=for-the-badge&logo=pytorch&logoColor=white)](https://pytorch.org/)
[![FAISS](https://img.shields.io/badge/FAISS-IndexFlatIP-00A4EF?style=for-the-badge)](https://github.com/facebookresearch/faiss)

An enterprise-grade, high-throughput asynchronous transcreation, multimodal asset rendering, and semantic content discovery engine. Specially designed for regional localization and contextual promotional ingestion pipelines within multi-lingual audio entertainment and over-the-top (OTT) media-streaming networks.

---

## 🛠️ System Architecture

The pipeline implements a **Decoupled Asynchronous Multimodal Orchestrator** framework to separate high-latency cloud operations and blocking file mutations from the hot loop of user-facing interfaces.


```

```
              ┌──────────────────────────────────────────────┐
              │            Your Local Computer               │
              │                                              │

```

[Streamlit UI] ──>│ [FastAPI Backend] ──(Local FAISS Vector DB)  │
└──────┬───────────────────────┬───────────────┘
│ (Secure HTTP API)     │ (Network Voice I/O)
▼                       ▼
[Google Gemini API]        [Google TTS Endpoints]
(Cloud Intelligence)        (Synthetic Audio Generation)

```

1. **User Client Core (Streamlit Interface):** Exposes an intuitive, reactive, parameter-driven web portal split into an episodic localized creator panel, semantic search discovery matrix, and unified log visualization tables.
2. **Orchestration Gateway (FastAPI Microservice):** Coordinates background operations natively via structured HTTP requests secured by explicit header key validations (`X-API-KEY`). Offloads blocking sync work to thread pools to maintain a non-blocking Event Loop.
3. **Transcreation Core (Google GenAI Engine):** Adapts underlying creative properties culturally into target linguistic dialects using **Gemini 2.5 Flash** constrained strictly to a validated, runtime-enforced Pydantic payload serialization schema.
4. **Asynchronous Audio Renderer (gTTS + Executor Pools):** Offloads speech track synthesis tasks cleanly into isolated background daemon worker nodes, protecting files using an OS-level atomic temporary file-swapping pattern.
5. **Contextual Ingestion Vector Index (Normalized FAISS Core):** Projects unstructured promotional trailer summary hooks into 384-dimensional dense semantic spaces using a `SentenceTransformer` model, executing similarity rankings via a thread-safe FAISS Inner Product index.

---

## 📂 Production Directory Tree Layout

The workspace is cleanly segmented according to professional software development and MLOps standards:

```plaintext
Text to Voice Project/
├── .env                  # Local decrypted hardware connection strings & keys
├── .gitignore            # Version control filters excluding large binaries/caches
├── config.py             # Central runtime constants & fail-fast absolute environment validation
├── requirements.txt      # Strictly frozen package dependency manifest with CPU-optimized flags
├── api/
│   └── main.py           # Production FastAPI gateway lifecycle setup & request routers
├── app/
│   └── dashboard.py      # Hardened Streamlit frontend creator and diagnostic dashboard
├── src/
│   ├── translation_engine.py  # LLM transcreation engine & structured schema wrappers
│   ├── voice_synthesis.py     # Thread-isolated synthetic speech caching pipeline
│   └── search_indexing.py     # Normalized FAISS vector database & Cosine similarity lookups
├── data/                 # Local data lake structures (automatically ignored by git)
│   ├── audio_cache/      # Atomic SHA-256 fingerprinted .mp3 localized sound output assets
│   ├── raw_scripts/      # Archive storage logs for imported historical scripts
│   ├── pipeline_history.db    # Persistent indexed relational storage audit log records
│   ├── faiss_index.bin        # Serialized memory snap of FAISS geometric structures
│   └── vector_metadata.pkl    # Serialized map matching vector positions to context entries
└── logs/
    └── audix_system.log  # Central thread-safe logging terminal file appender stream

```

---

## 🔧 Core Modular Implementations

### 1. Central Configuration (`config.py`)

Centralizes initialization routines and triggers a defensive **Fail-Fast Pattern** during server boot. If required keys like `GEMINI_API_KEY` are missing or unreadable, the application aborts startup immediately with a descriptive tracking error, rather than failing silently later.

### 2. Transcreation Layer (`src/translation_engine.py`)

Handles cultural adaptation rather than simple literal word translation. Implements **Tenacity-driven Exponential Backoff Retries** (capped at 4 attempts with automatic intervals scaling up to 10s) to handle cloud throttling. Enforces type-safety on model outputs by utilizing Pydantic's `BaseModel` parsing hooks.

### 3. Asynchronous Audio Generation (`src/voice_synthesis.py`)

Generates unique, collision-resistant deterministic fingerprints of incoming strings using **SHA-256 hashing**. Matches duplicate requests instantly via file-system lookups to achieve zero-latency performance. Offloads the network-bound gTTS file mutations to background threads via a specialized `ThreadPoolExecutor` pool to eliminate event loop stalling. Uses an **Atomic File Swapping Pattern** (`tempfile.NamedTemporaryFile` + `shutil.move`) to protect against cache corruption if the engine drops out mid-write.

### 4. Mathematical Search Matrix (`src/search_indexing.py`)

Encodes text data into a 384-dimensional continuous vector layout using `SentenceTransformer('all-MiniLM-L6-v2')`. Normalizes spatial positions down to unit length via Euclidean L2 metrics, transforming standard **FAISS Inner Product (IndexFlatIP)** calculations directly into pure **Cosine Similarity**. Implements concurrency control via a `threading.Lock()` mutex loop to prevent memory race-conditions during simultaneous user write-ops.

### 5. FastAPI Service Gateway (`api/main.py`)

Exposes highly secured endpoints managed via custom application lifecycles. Uses modern `@asynccontextmanager` definitions to guarantee clean background pool initialization and resource teardown operations. Uses `asyncio.to_thread` wrappers to isolate synchronous CPU-heavy model evaluations cleanly into background workers.

---

## 🛠️ Step-by-Step Local Deployment & Execution Manual

Follow this layout to boot your ecosystem up seamlessly:

### Step 1: Clone Your Work Directory & Initialize Environment

```cmd
d:
cd "D:\GEN AI Projects\Text to Voice Project"
conda activate text_to_voice_env

```

### Step 2: Configure Your Security and Key Registries

Create a file named `.env` in the root folder and paste the exact block configuration (ensuring zero space artifacts on either side of the assignment parameters):

```env
GEMINI_API_KEY=AIzaSy...YourKey...
API_BEARER_TOKEN=testtoken123
API_BACKEND_URL=[http://127.0.0.1:8000](http://127.0.0.1:8000)

```

### Step 3: Launch Terminal A (The Asynchronous FastAPI Gateway Node)

Open a fresh Anaconda Command Prompt shell window and execute:

```cmd
d:
cd "D:\GEN AI Projects\Text to Voice Project"
conda activate text_to_voice_env
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload

```

*Verify that the console returns:* `INFO: Application startup complete.`

### Step 4: Launch Terminal B (The Deployed User Dashboard UI Console)

Open a completely separate parallel window pane configuration and execute:

```cmd
d:
cd "D:\GEN AI Projects\Text to Voice Project"
conda activate text_to_voice_env
streamlit run app/dashboard.py

```

*The web browser workspace interface automatically launches live to point directly at:* `http://localhost:8501`

### Step 5: Execute End-to-End System Tests

1. **Localization Check:** Go to Tab 1, enter a title, choose a regional dialect (e.g., Hindi/Tamil), paste your script text, and click **Run Production Pipeline**. Listen to the immediate output.
2. **Semantic Query Test:** Jump to Tab 2, search for abstract conceptual ideas (e.g., "A tense corporate thriller dealing with stock market manipulations"), and verify that the local FAISS tracking blocks return sub-millisecond similarity lookups.
3. **Audit Inspection:** Move to Tab 3 and click **Fetch Current System Records** to pull historical logging fields straight out of your local SQLite database.

---

## 📈 Enterprise MLOps Best Practices Built In

* **Central Instrumentation Logger:** All components funnel into a single, unified file appender logging interface (`logs/audix_system.log`) using explicit standard library streams, making debugging simple.
* **Production Error Masking:** Protects sensitive internal details by intercepting backend exceptions, saving detailed tracebacks to the server log file while serving generic, safe HTTP messages to the client.
* **Atomic Workspace Version Control:** Leverages a strictly defined `.gitignore` stack to automatically prevent deep directory files, databases, or multi-gigabyte audio blobs from accidentally uploading to public cloud spaces.

---

## 📄 License

Distributed under an enterprise-grade private software architecture blueprint license pattern. All rights reserved by the engineering development team.

```

```
