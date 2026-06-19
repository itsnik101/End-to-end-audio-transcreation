import hashlib
import os
import tempfile
import shutil
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
from gtts import gTTS
from config import AUDIO_CACHE_DIR

logger = logging.getLogger("audix.voice")

class VoiceSynthesisEngine:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)

    async def generate_audio_track_async(self, text: str, language_code: str) -> str:
        text_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()
        filename = f"{language_code}_{text_hash}.mp3"
        file_path = AUDIO_CACHE_DIR / filename

        if file_path.exists():
            logger.info(f"Cache Hit: Found matching audio file asset: {filename}")
            return filename

        lang_mapping = {"Hindi": "hi", "Tamil": "ta", "Telugu": "te", "English": "en"}
        iso_code = lang_mapping.get(language_code, "en")

        def _blocking_tts():
            logger.info("Executing network audio request via gTTS context pool.")
            tts = gTTS(text=text, lang=iso_code, slow=False)
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3", dir=str(AUDIO_CACHE_DIR)) as tmp:
                tmp_path = tmp.name
                
            try:
                tts.save(tmp_path)
                shutil.move(tmp_path, str(file_path))
                logger.info(f"Committed transactional audio node safely: {file_path}")
            except Exception as e:
                logger.error(f"Atomic system cache swap operation failure: {e}", exc_info=True)
                if os.path.exists(tmp_path):
                    os.unlink(tmp_path)
                raise e
            return filename

        loop = asyncio.get_running_loop()
        return await loop.run_in_executor(self.executor, _blocking_tts)

    def shutdown(self):
        logger.info("Flushing thread pools clean for application exit sequence.")
        self.executor.shutdown(wait=True)