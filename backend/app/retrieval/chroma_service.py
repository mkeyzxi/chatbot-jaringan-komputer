import os
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from app.core.config import settings

class ChromaService:
    def __init__(self):
        self.embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)
        
        # Absolute path calculation to ensure it works regardless of where the app is run
        base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
        persist_dir = os.path.join(base_dir, "data", "chroma")
        
        self.vectorstore = Chroma(
            collection_name=settings.chroma_collection,
            embedding_function=self.embeddings,
            persist_directory=persist_dir
        )
    
    def search(self, query: str, k: int = settings.retrieval_k):
        """Perform semantic search for Top-K chunks."""
        # Using similarity search with score
        docs_and_scores = self.vectorstore.similarity_search_with_score(query, k=k)
        return docs_and_scores

# Singleton instance
chroma_service = ChromaService()
