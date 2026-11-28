from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

    # Строка подключения к базе (из твоего .env)
    prime_db_dsn: str

    # Остальные настройки со значениями по умолчанию
    telegram_bot_token: str = ""
    telegram_chat_id: str = ""
    replay_start_date: str = "2025-01-06"
    data_dir: str = "data"
    timezone: str = "UTC"