from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List, Optional
from app.crud.book import create_book, get_books, get_book, update_book, delete_book, bulk_upload_books, search_books
from app.schemas.book import BookCreate, BookResponse, BookUpdate
from app.dependencies import get_db, get_current_user

router = APIRouter()

@router.post("/", response_model=BookResponse, status_code=status.HTTP_201_CREATED)
async def create_book_endpoint(book: BookCreate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await create_book(db, book)

@router.get("/", response_model=List[BookResponse])
async def get_books_endpoint(
    db: AsyncSession = Depends(get_db),
    skip: int = 0,
    limit: int = 10,
    sort_by: str = "title",
    title: Optional[str] = None,
    author: Optional[str] = None,
    genre: Optional[str] = None,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None
):
    return await get_books(db, skip, limit, sort_by, title, author, genre, year_from, year_to)

@router.get("/{book_id}", response_model=BookResponse)
async def get_book_endpoint(book_id: str, db: AsyncSession = Depends(get_db)):
    book = await get_book(db, book_id)
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    return book

@router.put("/{book_id}", response_model=BookResponse)
async def update_book_endpoint(book_id: str, book: BookUpdate, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    updated_book = await update_book(db, book_id, book)
    if not updated_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return updated_book

@router.delete("/{book_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book_endpoint(book_id: str, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    success = await delete_book(db, book_id)
    if not success:
        raise HTTPException(status_code=404, detail="Book not found")

@router.post("/bulk-upload", response_model=List[BookResponse])
async def bulk_upload_books_endpoint(books: List[BookCreate], db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    return await bulk_upload_books(db, books)

@router.get("/search", response_model=List[BookResponse])
async def search_books_endpoint(query: str, db: AsyncSession = Depends(get_db)):
    return await search_books(db, query)
