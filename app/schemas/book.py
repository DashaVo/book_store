from pydantic import BaseModel, Field, validator
from typing import List, Optional
from datetime import datetime
import uuid

class BookBase(BaseModel):
    title: str = Field(..., min_length=1)
    published_year: int = Field(..., ge=1800, le=datetime.now().year)
    genres: List[str] = Field(..., min_items=1)

    @validator("genres")
    def validate_genres(cls, v):
        valid_genres = ["Fiction", "Non-Fiction", "Science", "Fantasy", "Biography"]
        if not all(genre in valid_genres for genre in v):
            raise ValueError("Invalid genre")
        return v

class BookCreate(BookBase):
    author_names: List[str] = Field(..., min_items=1, min_length=1)

class BookUpdate(BookBase):
    title: Optional[str] = Field(None, min_length=1)
    published_year: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    genres: Optional[List[str]] = Field(None, min_items=1)
    author_names: Optional[List[str]] = Field(None, min_items=1, min_length=1)

class BookResponse(BookBase):
    id: uuid.UUID
    authors: List[str]

    class Config:
        from_attributes = True