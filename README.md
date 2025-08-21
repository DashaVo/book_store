# 📚 Book Management System

A modern **FastAPI-based** book management system powered by **PostgreSQL**, **SQLAlchemy**, and **JWT authentication**. This project provides a RESTful API for managing books with robust features like bulk uploads, fuzzy search, and secure endpoints.

## ✨ Features

- **RESTful API**: Perform CRUD operations on books (create, read, update, delete).
- **Bulk Upload**: Import multiple books via JSON.
- **Fuzzy Search**: Search books by title or author name (case-insensitive).
- **Secure Authentication**: JWT-based authentication for protected endpoints.
- **Data Validation**: Pydantic enforces non-empty strings, valid genres, and year range (1800–present).
- **Async Database**: Efficient async operations with SQLAlchemy and asyncpg.
- **Docker Support**: Run the application and database in containers with Docker Compose.

## 🛠 Prerequisites

- **Python**: 3.10 or higher
- **PostgreSQL**: 13 or higher (or use Docker)
- **Docker and Docker Compose**: For containerized setup
- **Git**: For cloning the repository

## 🚀 Setup (Local)

1. **Clone the Repository**:
   ```bash
   git clone <repository-url>
   cd book_store 
```
2. **Create a Virtual Environment**:
    
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
    
    - Install PostgreSQL locally or use Docker:
        
        ```bash
        docker run --name book_db -e POSTGRES_PASSWORD=password -d -p 5432:5432 postgres
        ```
        
    - Create the database:
        
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
        
6. **Run Database Migrations**:
    
    ```bash
    alembic upgrade head
    ```
    
7. **Start the Application**:
    
    ```bash
    uvicorn app.main:app --reload
    ```
    

## 🐳 Setup (Docker)

1. **Clone the Repository**:
    
    ```bash
    git clone <repository-url>
    cd book_store
    ```
    
2. **Build and Run with Docker Compose**:
    
    ```bash
    docker-compose up --build
    ```
    
3. **Run Migrations**:
    
    - Access the app container:
        
        ```bash
	    docker-compose -p book_store exec -it app bash
        ```
        
    - Run migrations inside the container:
        
        ```bash
        alembic upgrade head
        ```
        

## 🌐 Access the API

- **Swagger UI**: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs) or [http://localhost:8000/docs](http://localhost:8000/docs)
- **API Root**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/) or [http://localhost:8000/](http://localhost:8000/)

## 🔗 API Endpoints

|Method|Endpoint|Description|Authentication|
|---|---|---|---|
|POST|`/auth/register`|Register a user (`username`, `password`)|None|
|POST|`/auth/login`|Obtain JWT token (`username`, `password`)|None|
|POST|`/api/v1/books/`|Create a book (`title`, `published_year`, `genres`, `author_names`)|JWT|
|GET|`/api/v1/books/`|List books (supports `skip`, `limit`, `sort_by`, `title`, `author`, `genre`, `year_from`, `year_to`)|None|
|GET|`/api/v1/books/{book_id}`|Get book by UUID|None|
|PUT|`/api/v1/books/{book_id}`|Update book|JWT|
|DELETE|`/api/v1/books/{book_id}`|Delete book (and authors with no books)|JWT|
|POST|`/api/v1/books/bulk-upload`|Bulk upload books (JSON list)|JWT|
|GET|`/api/v1/books/search/`|Fuzzy search by title or author (`query`)|None|

## 🗄 Database Schema

- **users**:
    - `id`: UUID, primary key
    - `username`: String, unique
    - `hashed_password`: String (Bcrypt)
- **books**:
    - `id`: UUID, primary key
    - `title`: String
    - `published_year`: Integer
    - `genres`: String array
- **authors**:
    - `id`: UUID, primary key
    - `name`: String, unique
- **book_authors**:
    - `book_id`: UUID, foreign key (books.id)
    - `author_id`: UUID, foreign key (authors.id)

