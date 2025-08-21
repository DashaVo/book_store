
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
- PostgreSQL 13+ (or Docker for containerized setup)
- Docker and Docker Compose (for containerized setup)

## Setup (Local)

1. **Clone Repository**:
   ```bash
   git clone <repository-url>
   cd book_store
```

2. **Create Virtual Environment**:
    
    ```bash
    python -m venv .venv
    .venv\Scripts\activate  # Windows
    # source .venv/bin/activate  # Linux/Mac
    ```
    
3. **Install Dependencies**:
    
    ```bash
    pip install -r requirements.txt
    ```
    
4. **Set Up PostgreSQL**:
    
    - Install PostgreSQL or use Docker:
        
        ```bash
        docker run --name book_db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres
        ```
        
    - Create database:
        
        ```bash
        createdb -h localhost -U postgres book_db
        ```
        
5. **Configure Environment**:
    
    - Copy `.env.example` to `.env`:
        
        ```bash
        copy .env.example .env  # Windows
        # cp .env.example .env  # Linux/Mac
        ```
        
    - Edit `.env` with your PostgreSQL credentials and a secure JWT secret:
        
        ```env
        DATABASE_URL=postgresql+asyncpg://postgres:password@localhost:5432/book_db
        JWT_SECRET=your-secure-random-string-64-characters-long-or-more
        ```
        
    - Generate a JWT secret:
        
        ```bash
        python -c "import secrets; print(secrets.token_urlsafe(64))"
        ```
        
6. **Run Migrations**:
    
    ```bash
    set PYTHONPATH=C:\Users\Admin\PycharmProjects\book_store;%PYTHONPATH%  # Windows
    # export PYTHONPATH=$(pwd):$PYTHONPATH  # Linux/Mac
    alembic revision --autogenerate -m "create tables"
    alembic upgrade head
    ```
    
7. **Run Application**:
    
    ```bash
    uvicorn app.main:app --reload
    ```
    

## Setup (Docker)

1. **Build and Run with Docker Compose**:
    
    ```bash
    docker-compose up --build
    ```
    
2. **Run Migrations**:
    
    - Access the app container:
        
        ```bash
        docker-compose -p book_store exec -it app bash
        ```
        
    - Run migrations inside the container:
        
        ```bash
        alembic upgrade head
        ```
        
## Access API:
    
    - Swagger UI: `http://127.0.0.1:8000/docs`
    - API root: `http://127.0.0.1:8000/`
or 
    - Swagger UI: `http://localhost:8000/docs`
    - API root: `http://localhost:8000/`
    
## API Endpoints

- **POST /auth/register**: Register a user (`username`, `password`).
- **POST /auth/login**: Obtain JWT token (`username`, `password`).
- **POST /api/v1/books/**: Create a book (authenticated; requires `title`, `published_year`, `genres`, `author_names`).
- **GET /api/v1/books/**: List books (supports `skip`, `limit`, `sort_by`, `title`, `author`, `genre`, `year_from`, `year_to`).
- **GET /api/v1/books/{book_id}**: Get book by UUID.
- **PUT /api/v1/books/{book_id}**: Update book (authenticated).
- **DELETE /api/v1/books/{book_id}**: Delete book and authors with no remaining books (authenticated).
- **POST /api/v1/books/bulk-upload**: Bulk upload books (authenticated; JSON list).
- **GET /api/v1/books/search/**: Fuzzy search by title or author (`query` parameter).

## Database Schema

- **users**: `id` (UUID, PK), `username` (string, unique), `hashed_password` (string).
- **books**: `id` (UUID, PK), `title` (string), `published_year` (integer), `genres` (string array).
- **authors**: `id` (UUID, PK), `name` (string, unique).
- **book_authors**: `book_id` (UUID, FK), `author_id` (UUID, FK).
