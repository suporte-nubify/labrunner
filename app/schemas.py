from datetime import datetime

from pydantic import BaseModel, Field


class NoteBase(BaseModel):
    title: str = Field(..., max_length=200)
    content: str = Field(..., max_length=2000)


class NoteCreate(NoteBase):
    pass


class NoteRead(NoteBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


