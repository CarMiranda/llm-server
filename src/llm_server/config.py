import typing as t

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    port: int = 3000
    host: str = "0.0.0.0"
    device: t.Literal["cpu", "cuda"] = "cuda"
    max_context: int = 100


settings = Settings()
