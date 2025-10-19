from pydantic_settings import BaseSettings

class DatabaseSettings(BaseSettings):

    #Chroma vector db configuration
    chroma_mode: str = "persistent"
    chroma_db_path: str = "data/chroma"
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    # Postgres DB configuration
    db_type: str = "sqlite"
    db_user: str | None = None
    db_password: str | None = None
    db_host: str | None = None
    db_port: int | None = None
    db_name: str | None = None
    sqlite_path: str = "knowledge_base_local.db"

    model_config = {
        "extra": "allow",
        "env_file": ".env"
    }

settings = DatabaseSettings()
