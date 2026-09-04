import os
import sys
from pypdf import PdfReader
from typing import List
from dotenv import load_dotenv

# Add parent directory to path so we can import from app
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from app.core.config import settings
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def extract_text_from_pdf(pdf_path: str) -> List[Document]:
    """Extract text from PDF using pypdf and return as LangChain Documents."""
    documents = []
    try:
        reader = PdfReader(pdf_path)
        for page_num, page in enumerate(reader.pages):
            text = page.extract_text()
            
            # Basic text cleaning could be added here
            if text and text.strip():
                metadata = {
                    "source": os.path.basename(pdf_path),
                    "page": page_num + 1,
                    "domain": "jaringan_komputer",
                    "document_type": "modul",
                    "ingestion_version": "v1"
                }
                documents.append(Document(page_content=text, metadata=metadata))
        print(f"Extracted {len(documents)} pages from {os.path.basename(pdf_path)}")
    except Exception as e:
        print(f"Error reading {pdf_path}: {e}")
    return documents

def ingest_documents():
    """Main ingestion pipeline."""
    documents_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "documents")
    
    if not os.path.exists(documents_dir):
        print(f"Directory {documents_dir} does not exist.")
        return

    all_docs = []
    for filename in os.listdir(documents_dir):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(documents_dir, filename)
            all_docs.extend(extract_text_from_pdf(file_path))

    if not all_docs:
        print("No documents found to ingest.")
        return

    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=settings.chunk_size,
        chunk_overlap=settings.chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    
    chunks = text_splitter.split_documents(all_docs)
    
    # Add chunk_index to metadata
    for i, chunk in enumerate(chunks):
        chunk.metadata["chunk_index"] = i
        
    print(f"Created {len(chunks)} chunks.")

    # Embedding
    print(f"Loading embedding model {settings.embedding_model}...")
    embeddings = HuggingFaceEmbeddings(model_name=settings.embedding_model)

    # Vector Storage
    persist_directory = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "chroma")
    print(f"Saving to ChromaDB at {persist_directory}...")
    
    vectorstore = Chroma.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=settings.chroma_collection,
        persist_directory=persist_directory
    )
    
    print("Ingestion complete.")

if __name__ == "__main__":
    ingest_documents()
