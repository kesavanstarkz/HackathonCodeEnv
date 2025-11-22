from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET: str
    JWT_ALGORITHM: str = "HS256"
    AWS_LAMBDA_FUNCTION: str
    AWS_REGION: str = "ap-south-1"
    AZURE_FUNCTION_URL: str = "local"
    AZURE_FUNCTION_KEY: str = ""

    model_config = SettingsConfigDict(env_file=".env")

settings = Settings()
