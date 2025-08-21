# Book Management System

A FastAPI-based book management system with PostgreSQL, SQLAlchemy, and JWT authentication.

## Features
- RESTful API for CRUD operations on books.
- Bulk upload of books via JSON.
- Fuzzy search by title or author name.
- JWT-based authentication for secure endpoints.
- Pydantic validation for non-empty strings, valid genres, and year range (1800–current).
- Async database operations with SQLAlchemy and asyncpg.

## Prerequisites
- Python 3.10+
- PostgreSQL 13+
- Docker (optional, for PostgreSQL)

## Setup

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd book_store


Create Virtual Environment:
python -m venv .venv
.venv\Scripts\activate  # Windows
# source .venv/bin/activate  # Linux/Mac


Install Dependencies:
pip install -r requirements.txt


Set Up PostgreSQL:

Install PostgreSQL or use Docker:docker run --name book_db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres


Create database:createdb -h localhost -U postgres book_db


Configure Environment:

Copy .env.example to .env:copy .env.example .env  # Windows
# cp .env.example .env  # Linux/Mac


Edit .env with your PostgreSQL credentials and a secure JWT secret:  
DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/book_db
JWT_SECRET=your-secure-random-string-64-characters-long-or-more


Generate a JWT secret:python -c "import secrets; print(secrets.token_urlsafe(64))"




Run Migrations:
alembic revision --autogenerate -m "create tables"
alembic upgrade head


Run Application:
uvicorn app.main:app --reload


Access API:

Swagger UI: http://127.0.0.1:8000/docs
API root: http://127.0.0.1:8000/



API Endpoints

POST /auth/register: Register a user (username, password).
POST /auth/login: Obtain JWT token (username, password).
POST /api/v1/books/: Create a book (authenticated; requires title, published_year, genres, author_names).
GET /api/v1/books/: List books (supports skip, limit, sort_by, title, author, genre, year_from, year_to).
GET /api/v1/books/{book_id}: Get book by UUID.
PUT /api/v1/books/{book_id}: Update book (authenticated).
DELETE /api/v1/books/{book_id}: Delete book and authors with no remaining books (authenticated).
POST /api/v1/books/bulk-upload: Bulk upload books (authenticated; JSON list).
GET /api/v1/books/search/: Fuzzy search by title or author (query parameter).



Database Schema

users: id (UUID, PK), username (string, unique), hashed_password (string).
books: id (UUID, PK), title (string), published_year (integer), genres (string array).
authors: id (UUID, PK), name (string, unique).
book_authors: book_id (UUID, FK), author_id (UUID, FK).


