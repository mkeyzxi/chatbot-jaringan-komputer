from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    app_name: str = "chatbot-jaringan-komputer"
    app_env: str = "development"
    app_host: str = "0.0.0.0"
    app_port: int = 8000

    frontend_url: str = "http://localhost:5173"

    embedding_model: str = "intfloat/multilingual-e5-small"
    chunk_size: int = 1000
    chunk_overlap: int = 200

    vector_db: str = "chroma"
    chroma_persist_directory: str = "./data/chroma"
    chroma_collection: str = "jaringan-komputer"
    retrieval_k: int = 5

    default_llm_mode: str = "berpikir"
    llm_provider: str = "gemini"
    llm_model: str = "gemini-2.0-flash"
    fast_llm_provider: str = "groq"
    fast_llm_model: str = "openai/gpt-oss-120b"
    thinking_llm_provider: str = "gemini"
    thinking_llm_model: str = "gemini-2.0-flash"
    llm_temperature: float = 0.1
    llm_top_p: float = 0.9

    google_api_key: str = ""
    gemini_api_key: str = ""
    groq_api_key: str = ""

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )


settings = Settings()
