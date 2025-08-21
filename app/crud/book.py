from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from app.models.model_base import Book, Author, book_authors
from app.schemas.book import BookCreate, BookUpdate
from sqlalchemy.sql import func
from typing import List, Optional

async def create_book(db: AsyncSession, book: BookCreate):
    # Create or get authors
    author_objs = []
    for name in book.author_names:
        author = (await db.execute(select(Author).filter_by(name=name))).scalar_one_or_none()
        if not author:
            author = Author(name=name)
            db.add(author)
        author_objs.append(author)
    await db.flush()

    # Create book
    db_book = Book(title=book.title, published_year=book.published_year, genres=book.genres)
    db.add(db_book)
    await db.flush()

    # Link authors
    for author in author_objs:
        await db.execute(book_authors.insert().values(book_id=db_book.id, author_id=author.id))
    await db.commit()
    return db_book

async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10, sort_by: str = "title",
                   title: Optional[str] = None, author: Optional[str] = None, genre: Optional[str] = None,
                   year_from: Optional[int] = None, year_to: Optional[int] = None):
    query = select(Book).offset(skip).limit(limit)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.join(book_authors).join(Author).filter(Author.name.ilike(f"%{author}%"))
    if genre:
        query = query.filter(Book.genres.contains([genre]))
    if year_from:
        query = query.filter(Book.published_year >= year_from)
    if year_to:
        query = query.filter(Book.published_year <= year_to)
    if sort_by:
        query = query.order_by(getattr(Book, sort_by))
    result = await db.execute(query)
    return result.scalars().all()

async def get_book(db: AsyncSession, book_id: str):
    result = await db.execute(select(Book).filter_by(id=book_id))
    return result.scalar_one_or_none()

async def update_book(db: AsyncSession, book_id: str, book_update: BookUpdate):
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "author_names":
            # Update authors
            await db.execute(delete(book_authors).where(book_authors.c.book_id == book_id))
            for name in value:
                author = (await db.execute(select(Author).filter_by(name=name))).scalar_one_or_none()
                if not author:
                    author = Author(name=name)
                    db.add(author)
                    await db.flush()
                await db.execute(book_authors.insert().values(book_id=book_id, author_id=author.id))
        else:
            setattr(db_book, key, value)
    await db.commit()
    return db_book

async def delete_book(db: AsyncSession, book_id: str):
    result = await db.execute(delete(Book).where(Book.id == book_id))
    await db.commit()
    return result.rowcount > 0

async def bulk_upload_books(db: AsyncSession, books: List[BookCreate]):
    created_books = []
    for book in books:
        created_book = await create_book(db, book)
        created_books.append(created_book)
    return created_books

async def search_books(db: AsyncSession, query: str):
    search_query = select(Book).join(book_authors).join(Author).filter(
        (Book.title.ilike(f"%{query}%")) | (Author.name.ilike(f"%{query}%"))
    )
    result = await db.execute(search_query)
    return result.scalars().all()
