from pydantic_settings import BaseSettings, SettingsConfigDict

# Определяем класс Settings, который наследуется от BaseSettings (из pydantic-settings).
# Этот класс будет автоматически загружать настройки из окружения или .env файла.
class Settings(BaseSettings):
    DB_HOST: str  # Обязательная настройка: хост базы данных (например, localhost).
    DB_PORT: int  # Обязательная настройка: порт базы данных (например, 5432 для PostgreSQL).
    DB_USER: str  # Обязательная настройка: имя пользователя для подключения к базе данных.
    DB_PASS: str  # Обязательная настройка: пароль для подключения к базе данных.
    DB_NAME: str  # Обязательная настройка: имя базы данных.

    # Свойство для формирования URL подключения к базе данных (для синхронного движка - psycopg)
    @property
    def DATABASE_URL_psyconf(self) -> str:
        """
        Формирует строку подключения к базе данных PostgreSQL с использованием драйвера psycopg.
        Эта строка используется для синхронного подключения к базе данных.
        """
        return f"postgresql+psycopg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Свойство для формирования URL подключения к базе данных (для асинхронного движка - asyncpg)
    @property
    def DATABASE_URL_asyncpg(self) -> str:
        """
        Формирует строку подключения к базе данных PostgreSQL с использованием асинхронного драйвера asyncpg.
        Эта строка используется для асинхронного подключения к базе данных.
        """
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    # Конфигурация модели pydantic-settings
    model_config = SettingsConfigDict(
        env_file=".env",  # Указываем имя файла, из которого будут загружаться переменные окружения.
        env_file_encoding="utf-8"  # Указываем кодировку файла .env.
    )

# Создаем экземпляр класса Settings. При этом будут автоматически загружены
# настройки из переменных окружения или файла .env.
settings = Settings()