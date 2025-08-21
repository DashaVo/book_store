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
        valid_genres = [
            "Fiction", "Non-Fiction", "Science", "Fantasy", "Biography",
            "Mystery", "Thriller", "Romance", "Historical", "Adventure",
            "Horror", "Science Fiction", "Dystopian", "Memoir", "Self-Help"
        ]
        if not all(genre in valid_genres for genre in v):
            raise ValueError("Invalid genre")
        return v

class BookCreate(BookBase):
    author_names: List[str] = Field(..., min_items=1)

    @validator("author_names", each_item=True)
    def validate_author_names(cls, v):
        if not v.strip():
            raise ValueError("Author name cannot be empty")
        return v.strip()

class BookUpdate(BookBase):
    title: Optional[str] = Field(None, min_length=1)
    published_year: Optional[int] = Field(None, ge=1800, le=datetime.now().year)
    genres: Optional[List[str]] = Field(None, min_items=1)
    author_names: Optional[List[str]] = Field(None, min_items=1)

    @validator("author_names", each_item=True)
    def validate_author_names(cls, v):
        if v is not None and not v.strip():
            raise ValueError("Author name cannot be empty")
        return v.strip() if v else v

class BookResponse(BookBase):
    id: uuid.UUID
    authors: List[str]

    @classmethod
    def from_orm(cls, obj):
        authors = [author.name for author in obj.authors]
        return cls(
            id=obj.id,
            title=obj.title,
            published_year=obj.published_year,
            genres=obj.genres,
            authors=authors
        )

    class Config:
        from_attributes = True