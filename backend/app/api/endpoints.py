from fastapi import APIRouter, HTTPException, status
from app.schemas.chat import ChatRequest, ChatResponse, RetrievalInfo, SourceMetadata
from app.retrieval.chroma_service import chroma_service
from app.generation.llm_service import llm_service
import time

router = APIRouter()

@router.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    start_time = time.time()
    
    query = request.question.strip()
    if not query:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Query cannot be empty")
        
    try:
        # Retrieve context
        retrieved_docs = chroma_service.search(query)
        
        # Build context string and source metadata
        context_texts = []
        sources = []
        
        for doc, score in retrieved_docs:
            context_texts.append(doc.page_content)
            # Create SourceMetadata safely
            src_meta = SourceMetadata(
                source=doc.metadata.get("source", "Unknown"),
                page=doc.metadata.get("page", 0),
                score=float(score)
            )
            sources.append(src_meta)
            
        combined_context = "\n\n---\n\n".join(context_texts)
        
        # Generate answer
        answer = llm_service.generate_answer(query, combined_context)
        
        latency_ms = (time.time() - start_time) * 1000
        
        return ChatResponse(
            answer=answer,
            retrieval=RetrievalInfo(
                k=len(sources),
                sources=sources
            ),
            latency_ms=latency_ms
        )
        
    except Exception as e:
        # Log error in real app
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=str(e))

@router.get("/health")
async def health_check():
    return {"status": "ok", "message": "Chatbot RAG API is healthy"}
