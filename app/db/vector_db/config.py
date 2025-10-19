from pydantic_settings import BaseSettings


class ChromeDbSettings(BaseSettings):
    chroma_mode: str = "persistent"
    chroma_db_path: str = "data/chroma"
    chroma_host: str = "localhost"
    chroma_port: int = 8000

    model_config = {
        "extra": "allow",
        "env_file": ".env"
    }


settings = ChromeDbSettings()
