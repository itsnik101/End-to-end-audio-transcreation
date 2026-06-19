import pytest
import faiss
from src.search_indexing import LocalVectorSearchEngine
from src.voice_synthesis import VoiceSynthesisEngine

def test_vector_search_cosine_similarity(tmp_path):
    engine = LocalVectorSearchEngine()
    engine.index_path = tmp_path / "faiss_index.bin"
    engine.metadata_path = tmp_path / "vector_metadata.pkl"
    engine.index = faiss.IndexFlatIP(384)
    engine.metadata_store = []
    
    engine.add_content_node(1, "A terrifying supernatural horror show about ghosts and small village curses", "Horror Show", "English")
    engine.add_content_node(2, "A sweet romantic comedy series where office workers fall deeply in love", "RomCom Show", "English")
    
    matches = engine.search_similar_stories("Chilling ghost thriller and paranormal activities", top_k=1)
    assert len(matches) == 1
    assert matches[0]["title"] == "Horror Show"

@pytest.mark.asyncio
async def test_voice_synthesis_async_generation():
    engine = VoiceSynthesisEngine()
    try:
        filename = await engine.generate_audio_track_async("Verification probe text", "English")
        assert filename.endswith(".mp3")
        assert "en_" in filename
    finally:
        engine.shutdown()