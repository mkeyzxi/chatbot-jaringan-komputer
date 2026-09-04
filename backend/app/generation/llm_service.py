from langchain_groq import ChatGroq
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings

class LLMService:
    def __init__(self):
        # Pass GROQ_API_KEY explicitly from settings
        self.llm = ChatGroq(
            model=settings.llm_model,
            temperature=settings.llm_temperature,
            groq_api_key=settings.groq_api_key,
            model_kwargs={"top_p": settings.llm_top_p}
        )
        
        self.system_instruction = """Anda adalah chatbot pembelajaran untuk mata kuliah Jaringan Komputer.

Tugas Anda adalah membantu mahasiswa memahami materi berdasarkan
konteks dokumen yang diberikan oleh sistem.

ATURAN UTAMA:
1. Gunakan konteks retrieval sebagai sumber utama jawaban.
2. Jangan mengarang fakta yang tidak didukung konteks.
3. Jika konteks tidak cukup untuk menjawab, katakan bahwa informasi
   yang diperlukan tidak tersedia pada materi yang diberikan.
4. Pertanyaan di luar domain pembelajaran Jaringan Komputer harus ditolak
   dengan sopan dan diarahkan kembali ke ruang lingkup sistem.
5. Jelaskan konsep dengan bahasa Indonesia yang mudah dipahami mahasiswa.
6. Untuk proses teknis seperti subnetting, tampilkan langkah yang relevan
   dan jangan menghilangkan asumsi penting."""

        self.prompt_template = ChatPromptTemplate.from_messages([
            ("system", self.system_instruction),
            ("user", "[CONTEXT]\n{retrieved_context}\n\n[USER QUESTION]\n{query}\n\n[INSTRUCTION]\nJawab pertanyaan pengguna hanya dengan memanfaatkan konteks yang tersedia.\nJika informasi tidak ditemukan atau tidak cukup, nyatakan keterbatasannya.")
        ])
        
        self.chain = self.prompt_template | self.llm | StrOutputParser()

    def generate_answer(self, query: str, context: str) -> str:
        """Generate answer using LLM based on retrieved context."""
        response = self.chain.invoke({
            "retrieved_context": context,
            "query": query
        })
        return response

# Singleton instance
llm_service = LLMService()
