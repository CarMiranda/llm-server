from pydantic import BaseModel


class Reply(BaseModel):
    message: str
