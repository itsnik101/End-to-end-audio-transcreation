# Text-to-Audio Localization Pipeline

A production-grade pipeline for culturally adapting and converting text scripts into regional audio content — built for multi-language audio entertainment platforms.

---

## What This Does

Takes an English or Hindi script, adapts it culturally for a target language (not just word-for-word translation), generates a synthesized audio track, and indexes it for semantic search — all through a web dashboard.

```
Input Script (English/Hindi)
        ↓
  Cultural Adaptation  →  Structured dialogue + marketing hook
        ↓
  Audio Generation     →  MP3 track per language
        ↓
  Vector Indexing      →  Searchable by concept/theme
```

---

## Tech Stack

| Layer | Tool |
|---|---|
| LLM Transcreation | Google Gemini 2.5 Flash |
| Text-to-Speech | gTTS (Google TTS) |
| Semantic Search | FAISS + SentenceTransformers |
| API Backend | FastAPI + aiosqlite |
| Dashboard | Streamlit |
| Logging | structlog |

---

## Project Structure

```
project-root/
├── api/
│   └── main.py              # FastAPI backend — endpoints & lifecycle
├── app/
│   └── dashboard.py         # Streamlit frontend
├── src/
│   ├── translation_engine.py  # Gemini-powered cultural adaptation
│   ├── voice_synthesis.py     # Async audio generation & caching
│   └── search_indexing.py     # FAISS vector search
├── data/
│   ├── raw_scripts/           # Uploaded scripts (auto-created)
│   └── audio_cache/           # Generated MP3s (auto-created)
├── tests/
│   └── test_pipeline.py       # Unit tests
├── config.py                  # Central config & environment validation
├── requirements.txt
└── .env                       # Your secret keys (not committed)
```

---

## Setup

### 1. Activate your environment

```bash
conda activate your_env_name
```

### 2. Install dependencies

```bash
pip install -r requirements.txt
```

### 3. Create a `.env` file in the project root

```env
GEMINI_API_KEY=your_gemini_key_here
API_BEARER_TOKEN=your_secure_token_here
API_BACKEND_URL=http://127.0.0.1:8000
```

Get a free Gemini API key at [aistudio.google.com](https://aistudio.google.com).

> The app will refuse to start if either key is missing — this is intentional.

---

## Running the App

Open **two terminals**, both in the project root with your environment activated.

**Terminal 1 — Start the backend:**

```bash
uvicorn api.main:app --host 127.0.0.1 --port 8000 --reload
```

Wait for: `INFO: Application startup complete.`

**Terminal 2 — Start the dashboard:**

```bash
streamlit run app/dashboard.py
```

Opens automatically at `http://localhost:8501`.

---

## Using the Dashboard

### Tab 1 — Localization Studio

1. Enter a show title
2. Select a target language (Hindi, Tamil, Telugu, English)
3. Paste your script
4. Click **Run Production Pipeline**

The pipeline returns:
- A 2-sentence promotional hook for the episode
- A synthesized audio track you can play in-browser
- The full adapted script with character names, dialogue, and emotional tone markers

### Tab 2 — Semantic Search

Search your indexed content by concept or theme — not just keywords.

Example: *"A tense corporate thriller with stock market betrayal"* will surface thematically similar shows even if they don't share any of those words.

### Tab 3 — History

Click **Fetch Current System Records** to see a table of all past pipeline runs pulled from the local SQLite database.

---

## Running Tests

```bash
pytest tests/
```

The test suite validates that the FAISS cosine similarity search returns semantically correct rankings (not just keyword matches).

---

## How Each Component Works

### Cultural Adaptation (not literal translation)

The Gemini model is instructed to adapt idioms, character names, jokes, and cultural references — not translate word-for-word. A character named "Robert" in an English script might become "Rajan" in a Tamil adaptation if it fits the regional context better.

Retries up to 4 times with exponential backoff (2s → 4s → 8s) on transient API failures. Will not retry on schema validation errors or bad inputs.

### Audio Caching

Each piece of text is hashed with SHA-256. If an identical text + language combination was already generated, the cached MP3 is returned instantly. New files are written atomically (temp file → rename) to prevent partial/corrupt audio if the process dies mid-write.

### Vector Search

Scripts are encoded into 384-dimensional vectors using `all-MiniLM-L6-v2`. Vectors are L2-normalized so that FAISS Inner Product scores become true cosine similarity rankings. The index is thread-safe — concurrent writes are serialized via a mutex lock, and disk persistence happens outside the lock to avoid blocking reads.

---

## Key Design Decisions

**Why not a task queue (Celery/arq)?**
For a portfolio/demo deployment, synchronous-within-async is acceptable. The Gemini call (5–15s) and TTS call (2–5s) are offloaded to thread pools, so the event loop stays unblocked. Under production load with many concurrent users, a proper task queue would be the next step.

**Why SQLite instead of Postgres?**
Zero infrastructure overhead for local/demo use. The history table is indexed on `target_language` for filtered queries. Migrating to Postgres later requires only changing the `aiosqlite` connection string.

**Why gTTS?**
Free, no billing ceiling, supports Hindi/Tamil/Telugu/English natively. The trade-off is audio quality — it sounds robotic compared to paid TTS APIs. Swapping in ElevenLabs or Google Cloud TTS requires only changing `voice_synthesis.py`.

---

## Limitations

- **Dashboard is synchronous**: Long pipeline runs (20–30s) keep the Streamlit spinner active but do not block other browser tabs
- **FAISS is in-memory**: The index loads fully on startup — fine for thousands of entries, not suitable for millions
- **gTTS quality**: Adequate for demos, not production audio entertainment
- **No background job queue**: One heavy request per user at a time; concurrent users share the thread pool

---

## License

Private project. All rights reserved.
