from fastapi import FastAPI
from app.routers import books, auth

app = FastAPI(title="Book Management System")

app.include_router(books.router, prefix="/api/v1/books", tags=["books"])
app.include_router(auth.router, prefix="/auth", tags=["auth"])

@app.get("/")
async def root():
    return {"message": "Book Management System API"}