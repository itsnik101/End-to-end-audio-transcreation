import numpy as np
import faiss
import pickle
import threading
import logging
from sentence_transformers import SentenceTransformer
from config import DATA_DIR

logger = logging.getLogger("audix.vector")

class LocalVectorSearchEngine:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index_path = DATA_DIR / "faiss_index.bin"
        self.metadata_path = DATA_DIR / "vector_metadata.pkl"
        
        self.dimension = 384
        self.metadata_store = []
        self.lock = threading.Lock()
        
        if self.index_path.exists() and self.metadata_path.exists():
            logger.info("Loading absolute binary vector matrix blocks from system disk storage.")
            self.index = faiss.read_index(str(self.index_path))
            with open(self.metadata_path, 'rb') as f:
                self.metadata_store = pickle.load(f)
            logger.info(f"Vector spatial maps tracking safely. Capacity count: {self.index.ntotal}")
        else:
            logger.info("Initializing baseline IndexFlatIP configurations for Cosine math metrics.")
            self.index = faiss.IndexFlatIP(self.dimension)

    def add_content_node(self, script_id: int, summary_text: str, title: str, language: str):
        logger.info(f"Computing 384 dimensional dense feature maps for script index: #{script_id}")
        embedding = self.model.encode([summary_text])[0].astype('float32')
        
        norm = np.linalg.norm(embedding)
        if norm > 0:
            embedding = embedding / norm

        with self.lock:
            self.index.add(np.array([embedding]))
            self.metadata_store.append({
                "script_id": script_id,
                "title": title,
                "summary": summary_text,
                "language": language
            })
            
        self._save_checkpoint_to_disk()

    def _save_checkpoint_to_disk(self):
        with self.lock:
            index_snapshot = faiss.serialize_index(self.index)
            metadata_snapshot = list(self.metadata_store)

        tmp_idx_path = self.index_path.with_suffix(".tmp")
        tmp_meta_path = self.metadata_path.with_suffix(".tmp")
        
        try:
            with open(tmp_idx_path, "wb") as f:
                f.write(index_snapshot)
            with open(tmp_meta_path, 'wb') as f:
                pickle.dump(metadata_snapshot, f)
                
            tmp_idx_path.replace(self.index_path)
            tmp_meta_path.replace(self.metadata_path)
            logger.info(f"Atomic database checkpoints completed cleanly. Total elements: {self.index.ntotal}")
        except Exception as e:
            logger.error(f"Failsafe triggered. Vector file save sequence failure: {e}", exc_info=True)
            if tmp_idx_path.exists(): tmp_idx_path.unlink()
            if tmp_meta_path.exists(): tmp_meta_path.unlink()

    def search_similar_stories(self, query: str, top_k: int = 3) -> list[dict]:
        if self.index.ntotal == 0:
            logger.warning("Empty matrix layout. Vector tracking lookup aborted.")
            return []
            
        logger.info(f"Running Cosine similarity tracking calculation query: '{query}'")
        query_vector = self.model.encode([query])[0].astype('float32')
        norm = np.linalg.norm(query_vector)
        if norm > 0:
            query_vector = query_vector / norm

        with self.lock:
            distances, indices = self.index.search(np.array([query_vector]), top_k)
        
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata_store):
                results.append(self.metadata_store[idx])
        return results