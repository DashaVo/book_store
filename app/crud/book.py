from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, func
from sqlalchemy.orm import joinedload
from app.models.model_base import Book, Author, book_authors
from app.schemas.book import BookCreate, BookUpdate
from typing import List, Optional


async def create_book(db: AsyncSession, book: BookCreate):
    author_objs = []
    for name in book.author_names:
        author = (await db.execute(select(Author).filter_by(name=name))).scalar_one_or_none()
        if not author:
            author = Author(name=name)
            db.add(author)
        author_objs.append(author)
    await db.flush()

    db_book = Book(title=book.title, published_year=book.published_year, genres=book.genres)
    db.add(db_book)
    await db.flush()

    for author in author_objs:
        await db.execute(book_authors.insert().values(book_id=db_book.id, author_id=author.id))

    result = await db.execute(select(Book).options(joinedload(Book.authors)).filter_by(id=db_book.id))
    db_book = result.unique().scalar_one()
    await db.commit()

    return db_book


async def get_books(db: AsyncSession, skip: int = 0, limit: int = 10, sort_by: str = "title",
                    title: Optional[str] = None, author: Optional[str] = None, genre: Optional[str] = None,
                    year_from: Optional[int] = None, year_to: Optional[int] = None):
    query = select(Book).options(joinedload(Book.authors)).offset(skip).limit(limit)
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    if author:
        query = query.join(book_authors).join(Author).filter(Author.name.ilike(f"%{author}%"))
    if genre:
        genres_list = genre.split(",") if genre else []
        if genres_list:
            query = query.filter(Book.genres.contains(genres_list))
    if year_from:
        query = query.filter(Book.published_year >= year_from)
    if year_to:
        query = query.filter(Book.published_year <= year_to)
    if sort_by:
        query = query.order_by(getattr(Book, sort_by))
    result = await db.execute(query)
    books = result.unique().scalars().all()
    return [{
        "id": book.id,
        "title": book.title,
        "published_year": book.published_year,
        "genres": book.genres,
        "authors": [author.name for author in book.authors]
    } for book in books]


async def get_book(db: AsyncSession, book_id: str):
    result = await db.execute(select(Book).options(joinedload(Book.authors)).filter_by(id=book_id))
    return result.unique().scalar_one_or_none()


async def update_book(db: AsyncSession, book_id: str, book_update: BookUpdate):
    db_book = await get_book(db, book_id)
    if not db_book:
        return None
    update_data = book_update.dict(exclude_unset=True)
    for key, value in update_data.items():
        if key == "author_names":
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
    result = await db.execute(select(Book).options(joinedload(Book.authors)).filter_by(id=book_id))
    return result.unique().scalar_one()


async def delete_book(db: AsyncSession, book_id: str):
    associated_authors_query = select(book_authors.c.author_id).where(book_authors.c.book_id == book_id)
    associated_authors_result = await db.execute(associated_authors_query)
    associated_authors = [row[0] for row in associated_authors_result.fetchall()]

    await db.execute(delete(book_authors).where(book_authors.c.book_id == book_id))
    result = await db.execute(delete(Book).where(Book.id == book_id))
    deleted_count = result.rowcount

    for author_id in associated_authors:
        remaining_books_query = select(func.count()).select_from(book_authors).where(
            book_authors.c.author_id == author_id)
        remaining_books_result = await db.execute(remaining_books_query)
        remaining_books = remaining_books_result.scalar()
        if remaining_books == 0:
            await db.execute(delete(Author).where(Author.id == author_id))

    await db.commit()
    return deleted_count > 0


async def bulk_upload_books(db: AsyncSession, books: List[BookCreate]):
    created_books = []
    for book in books:
        created_book = await create_book(db, book)
        created_books.append(created_book)
    return created_books


async def search_books(db: AsyncSession, query: str):
    search_query = select(Book).options(joinedload(Book.authors)).filter(
        (Book.title.ilike(f"%{query}%")) | (Author.name.ilike(f"%{query}%"))
    )
    result = await db.execute(search_query)
    books = result.unique().scalars().all()
    return [{
        "id": book.id,
        "title": book.title,
        "published_year": book.published_year,
        "genres": book.genres,
        "authors": [author.name for author in book.authors]
    } for book in books]