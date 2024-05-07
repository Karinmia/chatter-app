from pydantic import BaseModel


class Channel(BaseModel):
    id = str
    name: str


class Message(BaseModel):
    channel_id = str
    author: str
    content: str
    timestamp: int
    

class CreateMessage(BaseModel):
    content: str