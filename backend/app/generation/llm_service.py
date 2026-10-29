import os
from typing import Literal

from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_openai import ChatOpenAI

from app.core.config import settings


ModeType = Literal["cepat", "berpikir"]


class LLMService:
    def __init__(self):
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

        self.default_chain = self._build_chain_for_mode(settings.default_llm_mode)

    def _build_prompt_for_mode(self, mode: ModeType):
        if mode == "cepat":
            system_instruction = self.system_instruction + "\n\nMODE JAWABAN CEPAT:\n- Jawab singkat, padat, dan langsung ke inti.\n- Prioritaskan jawaban 1-3 paragraf atau beberapa poin singkat.\n- Hindari penjelasan yang tidak relevan atau terlalu panjang.\n- Jika perlu, gunakan poin-poin sederhana, bukan elaborasi berlebihan.\n- Jangan buat tabel kecuali pengguna benar-benar meminta."
            user_instruction = (
                "[CONTEXT]\n{retrieved_context}\n\n[USER QUESTION]\n{query}\n\n[INSTRUCTION]\n"
                "Jawab dengan ringkas, jelas, dan sesuai konteks yang tersedia.\n"
                "Jika informasi tidak ditemukan atau tidak cukup, nyatakan keterbatasannya secara singkat."
            )
        else:
            system_instruction = self.system_instruction + "\n\nMODE JAWABAN DETAIL:\n- Berikan jawaban yang lengkap, jelas, dan mudah dipahami.\n- Jelaskan konsep dengan detail yang cukup untuk mahasiswa.\n- Gunakan struktur logis seperti penjelasan singkat, langkah, contoh, dan kesimpulan.\n- Jika relevan, tampilkan tabel yang rapi untuk membandingkan atau merangkum konsep.\n- Sertakan asumsi penting untuk soal teknis seperti subnetting atau routing."
            user_instruction = (
                "[CONTEXT]\n{retrieved_context}\n\n[USER QUESTION]\n{query}\n\n[INSTRUCTION]\n"
                "Jawab dengan detail dan berdasarkan konteks yang tersedia.\n"
                "Gunakan bahasa Indonesia yang jelas.\n"
                "Jika informasi tidak ditemukan atau tidak cukup, nyatakan keterbatasannya dengan jujur.\n"
                "Jika ada perbandingan atau konsep yang perlu dirangkum, gunakan tabel bila relevan."
            )

        return ChatPromptTemplate.from_messages([
            ("system", system_instruction),
            ("user", user_instruction),
        ])

    def _get_api_key_for_mode(self, mode: ModeType) -> str:
        if mode == "cepat":
            return settings.groq_api_key or os.getenv("GROQ_API_KEY") or ""
        return settings.google_api_key or settings.gemini_api_key or os.getenv("GOOGLE_API_KEY") or os.getenv("GEMINI_API_KEY") or ""

    def _get_model_for_mode(self, mode: ModeType) -> str:
        if mode == "cepat":
            return settings.fast_llm_model or "openai/gpt-oss-120b"
        return settings.thinking_llm_model or settings.llm_model or "gemini-3.8-flash"
  
    def _get_provider_for_mode(self, mode: ModeType) -> str:
        if mode == "cepat":
            return settings.fast_llm_provider or "groq"
        return settings.thinking_llm_provider or settings.llm_provider or "gemini"

    def _build_chain_for_mode(self, mode: ModeType):
        provider = self._get_provider_for_mode(mode)
        api_key = self._get_api_key_for_mode(mode)
        model_name = self._get_model_for_mode(mode)

        if provider == "groq":
            if not api_key:
                raise ValueError("API key Groq belum diatur. Isi GROQ_API_KEY di file .env.")
            llm = ChatOpenAI(
                model=model_name,
                api_key=api_key,
                base_url="https://api.groq.com/openai/v1",
                temperature=settings.llm_temperature,
                top_p=settings.llm_top_p,
            )
        else:
            if not api_key:
                raise ValueError(
                    "API key Gemini belum diatur. Isi GOOGLE_API_KEY atau GEMINI_API_KEY di file .env."
                )
            llm = ChatGoogleGenerativeAI(
                model=model_name,
                google_api_key=api_key,
                temperature=settings.llm_temperature,
                top_p=settings.llm_top_p,
            )

        prompt_template = self._build_prompt_for_mode(mode)
        return prompt_template | llm | StrOutputParser()

    def _get_chain_for_mode(self, mode: ModeType):
        return self._build_chain_for_mode(mode)

    def generate_answer(self, query: str, context: str, mode: ModeType = None) -> str:
        """Generate answer using LLM based on retrieved context."""
        current_mode = mode or settings.default_llm_mode
        chain = self._get_chain_for_mode(current_mode)
        response = chain.invoke({
            "query": query,
            "retrieved_context": context,
        })
        return response


# Singleton instance
llm_service = LLMService()
