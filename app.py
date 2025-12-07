from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database import engine, Base, get_db
from schemas import BookCreate, Book
import crud

# --- Create database tables ---
Base.metadata.create_all(bind=engine)

# --- Create FastAPI app ---
app = FastAPI(title="Online Bookstore API")

# --- CORS setup ---
# During development, allow all origins to fix OPTIONS 400 issues
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],        # allow all origins during development
    allow_credentials=True,
    allow_methods=["*"],        # allow GET, POST, DELETE, OPTIONS
    allow_headers=["*"],        # allow Content-Type and all headers
)

# --- Routes ---
@app.get("/books", response_model=list[Book])
def read_books(db: Session = Depends(get_db)):
    return crud.get_books(db)

@app.post("/books", response_model=Book)
def add_book(book: BookCreate, db: Session = Depends(get_db)):
    return crud.create_book(db, book)

@app.get("/books/{book_id}", response_model=Book)
def read_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.get_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@app.delete("/books/{book_id}", response_model=Book)
def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = crud.delete_book(db, book_id)
    if db_book is None:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book
