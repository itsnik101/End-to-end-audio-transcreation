import sys
import os
from pathlib import Path

# Add project root directory explicitly to Python path initialization layout
# This ensures submodules resolve perfectly even when launched from nested child contexts
sys.path.append(str(Path(__file__).resolve().parent.parent))

import asyncio
import logging
import aiosqlite
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Security, Depends
from fastapi.security import APIKeyHeader
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field
from src.translation_engine import TranslationEngine
from src.voice_synthesis import VoiceSynthesisEngine
from src.search_indexing import LocalVectorSearchEngine
from config import DB_PATH, AUDIO_CACHE_DIR, API_BEARER_TOKEN

logger = logging.getLogger("audix.api")

translator = TranslationEngine()
voice_engine = VoiceSynthesisEngine()
search_engine = LocalVectorSearchEngine()

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing relational SQLite framework metrics schemas asynchronously.")
    try:
        async with aiosqlite.connect(str(DB_PATH)) as db:
            await db.execute('''
                CREATE TABLE IF NOT EXISTS production_history (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    original_title TEXT,
                    target_language TEXT,
                    summary TEXT,
                    structured_json TEXT,
                    audio_path TEXT
                )
            ''')
            await db.execute("CREATE INDEX IF NOT EXISTS idx_lang ON production_history(target_language)")
            await db.commit()
    except Exception as db_err:
        logger.critical(f"Database infrastructure startup aborted: {db_err}", exc_info=True)
        raise db_err
    yield
    logger.info("Terminating API orchestration interface operations context mapping.")
    voice_engine.shutdown()

app = FastAPI(title="AudiX Enterprise GenAI Pipeline", version="1.0.0", lifespan=lifespan)
app.mount("/static/audio", StaticFiles(directory=str(AUDIO_CACHE_DIR)), name="audio")

api_key_header = APIKeyHeader(name="X-API-KEY", auto_error=True)

async def verify_auth(api_key: str = Depends(api_key_header)):
    if api_key != API_BEARER_TOKEN:
        logger.warning("Security Exception: Authorization mismatch error encountered.")
        raise HTTPException(status_code=403, detail="Unauthorized client access credentials.")

class LocalizeRequest(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    raw_script: str = Field(..., min_length=10, max_length=50000)
    target_language: str = Field(..., min_length=2)

class QueryRequest(BaseModel):
    query_string: str = Field(..., min_length=3)

@app.post("/api/v1/localize", dependencies=[Depends(verify_auth)])
async def process_localization(payload: LocalizeRequest):
    logger.info(f"Processing inbound structural localization requests - Title: '{payload.title}'")
    try:
        localized_data = await asyncio.to_thread(
            translator.transcreate_script, payload.raw_script, payload.target_language, payload.title
        )
        
        full_dialogue_text = " . ".join([d.translated_dialogue for d in localized_data.dialogue_flow])
        audio_filename = await voice_engine.generate_audio_track_async(full_dialogue_text, payload.target_language)
        audio_serving_endpoint = f"/static/audio/{audio_filename}"
        
        async with aiosqlite.connect(str(DB_PATH)) as db:
            async with db.execute('''
                INSERT INTO production_history (original_title, target_language, summary, structured_json, audio_path)
                VALUES (?, ?, ?, ?, ?)
            ''', (payload.title, payload.target_language, localized_data.story_hook_summary, 
                  localized_data.model_dump_json(), audio_serving_endpoint)) as cursor:
                generated_id = cursor.lastrowid
            await db.commit()

        await asyncio.to_thread(
            search_engine.add_content_node,
            generated_id, localized_data.story_hook_summary, payload.title, payload.target_language
        )
        return {
            "status": "Success",
            "script_id": generated_id,
            "localized_content": localized_data.model_dump(),
            "audio_asset_url": audio_serving_endpoint
        }
    except Exception as e:
        logger.error(f"Critical execution error tracking inside orchestrator limits: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal processing failure within orchestration layer.")

@app.post("/api/v1/search", dependencies=[Depends(verify_auth)])
async def perform_search(payload: QueryRequest):
    try:
        matches = await asyncio.to_thread(search_engine.search_similar_stories, payload.query_string)
        return {"status": "Success", "results": matches}
    except Exception as e:
        logger.error(f"Vector database coordinate computation exception: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal search engine failure.")

@app.get("/api/v1/history", dependencies=[Depends(verify_auth)])
async def fetch_history():
    async with aiosqlite.connect(str(DB_PATH)) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM production_history ORDER BY id DESC LIMIT 100") as cursor:
            rows = await cursor.fetchall()
            return [dict(row) for row in rows]