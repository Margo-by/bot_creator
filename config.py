from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    TELEGRAM_BOT_TOKEN: str
    OPENAI_API_KEY: str
    ASSISTANT_ID: str
    VECTOR_STORE_ID: str

    class Config:
        env_file = '.env'


settings = Settings()


