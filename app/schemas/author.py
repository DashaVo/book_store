from pydantic import BaseModel, Field

class AuthorBase(BaseModel):
    name: str = Field(..., min_length=1)

class AuthorResponse(AuthorBase):
    id: str

    class Config:
        from_attributes = True