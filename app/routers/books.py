from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
import uuid
from app.crud.book import create_book, get_books, get_book, update_book, delete_book, bulk_upload_books, search_books
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED,
             description="Create a new book. Requires JWT authentication.")
async def create_book_endpoint(book: BookCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    db_book = await create_book(db, book)
    return BookResponse.from_orm(db_book)

@router.get("/",
            description="List books with pagination, sorting, and filtering. Parameters:\n"
                        "- **skip**: Number of records to skip (default: 0).\n"
                        "- **limit**: Maximum number of records to return (default: 10).\n"
                        "- **sort_by**: Sort by field (options: 'title', 'published_year'; default: 'title').\n"
                        "- **title**: Filter by book title (partial match, case-insensitive).\n"
                        "- **author**: Filter by author name (partial match, case-insensitive).\n"
                        "- **genre**: Filter by genres (comma-separated list, e.g., 'Fiction,Fantasy'; must be one of: Fiction, Non-Fiction, Science, Fantasy, Biography, Mystery, Thriller, Romance, Historical, Adventure, Horror, Science Fiction, Dystopian, Memoir, Self-Help).\n"
                        "- **year_from**: Filter by minimum published year.\n"
                        "- **year_to**: Filter by maximum published year.")
async def get_books_endpoint(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[List[str]] = Query(None, description="Comma-separated list of genres (e.g., 'Fiction,Fantasy')"),
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
):
    genre_str = ",".join(genre) if genre else None
    return await get_books(db, skip, limit, sort_by, title, author, genre_str, year_from, year_to)

@router.get("/search/",
            description="Fuzzy search books by title or author name (case-insensitive).\n"
                        "- **query**: Search term to match against book title or author name (e.g., 'Harry' for Harry Potter).")
async def search_books_endpoint(query: str, db: AsyncSession = Depends(get_db)):
    return await search_books(db, query)

@router.get("/{book_id:uuid}", response_model=BookResponse,
            description="Get a book by its UUID.")
async def get_book_endpoint(book_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, str(book_id))
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.from_orm(book)

@router.put("/{book_id:uuid}", response_model=BookResponse,
            description="Update a book by its UUID. Requires JWT authentication.")
async def update_book_endpoint(book_id: uuid.UUID, book: BookUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    updated_book = await update_book(db, str(book_id), book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return BookResponse.from_orm(updated_book)

@router.delete("/{book_id:uuid}", status_code=status.HTTP_204_NO_CONTENT,
               description="Delete a book by its UUID. Also deletes authors with no remaining books. Requires JWT authentication.")
async def delete_book_endpoint(book_id: uuid.UUID, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    success = await delete_book(db, str(book_id))
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/bulk-upload", response_model=List[BookResponse],
             description="Bulk upload multiple books. Requires JWT authentication.")
async def bulk_upload_books_endpoint(books: List[BookCreate], db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    created_books = await bulk_upload_books(db, books)
    return [BookResponse.from_orm(book) for book in created_books]