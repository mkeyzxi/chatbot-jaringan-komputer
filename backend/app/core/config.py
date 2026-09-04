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

    llm_provider: str = "groq"
    llm_model: str = "openai/gpt-oss-120b"
    llm_temperature: float = 0.1
    llm_top_p: float = 0.9

    groq_api_key: str = ""

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")

settings = Settings()
