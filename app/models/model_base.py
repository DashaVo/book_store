from sqlalchemy.ext.asyncio import AsyncAttrs
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy import Column, String, Integer, ARRAY, UUID, Table, ForeignKey
from sqlalchemy.orm import relationship
import uuid

class ModelBase(AsyncAttrs, DeclarativeBase):
    pass

class User(ModelBase):
    __tablename__ = "users"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String, unique=True, nullable=False)
    hashed_password = Column(String, nullable=False)

class Book(ModelBase):
    __tablename__ = "books"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    title = Column(String, nullable=False)
    published_year = Column(Integer)
    genres = Column(ARRAY(String))
    authors = relationship("Author", secondary="book_authors", back_populates="books")

book_authors = Table(
    "book_authors",
    ModelBase.metadata,
    Column("book_id", UUID(as_uuid=True), ForeignKey("books.id"), primary_key=True),
    Column("author_id", UUID(as_uuid=True), ForeignKey("authors.id"), primary_key=True)
)

class Author(ModelBase):
    __tablename__ = "authors"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False, unique=True)
    books = relationship("Book", secondary="book_authors", back_populates="authors")