"""FastAPI uygulaması (Aşama 3)
GET /books, POST /books, DELETE /books/{isbn}
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional, List
from pathlib import Path

from library import Library, Book
from open_library import OpenLibraryClient


app = FastAPI(title="Library API", version="1.0.0")
lib = Library()
client = OpenLibraryClient()

BASE_DIR = Path(__file__).resolve().parent
UI_INDEX = BASE_DIR / "ui" / "index.html"


## CORS kaldırıldı. UI aynı origin'den servis ediliyor.

@app.get("/")
def root():
    # Basit HTML arayüzünü servis et
    return FileResponse(UI_INDEX)


@app.get("/health")
def health():
    return {"status": "ok"}


class BookModel(BaseModel):
    title: str
    author: str
    isbn: str
    created_at: Optional[str] = None
    genres: Optional[List[str]] = None


class ISBNBody(BaseModel):
    isbn: str


@app.get("/books", response_model=list[BookModel])
def list_books():
    return [BookModel(title=b.title, author=b.author, isbn=b.isbn, created_at=b.created_at, genres=b.genres) for b in lib.list_books()]


@app.post("/books", response_model=BookModel, status_code=status.HTTP_201_CREATED)
def create_book(body: ISBNBody):
    try:
        book = lib.add_book_by_isbn(body.isbn, client)
        return BookModel(title=book.title, author=book.author, isbn=book.isbn)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


@app.delete("/books/{isbn}", status_code=status.HTTP_204_NO_CONTENT)
def delete_book(isbn: str):
    ok = lib.remove_book(isbn)
    if not ok:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Kitap bulunamadı")
    return None


class ISBNListBody(BaseModel):
    isbns: list[str]


@app.delete("/books", status_code=status.HTTP_200_OK)
def delete_books(body: ISBNListBody):
    deleted, not_found = lib.remove_books(body.isbns)
    return {"deleted": deleted, "not_found": not_found}


@app.get("/books/preview/{isbn}", response_model=BookModel)
def preview_book(isbn: str):
    try:
        norm = client.normalize_isbn_or_barcode(isbn)
        info = client.fetch_by_isbn(norm)
        title = info["title"]
        authors: list[str] = info.get("authors", [])
        author = ", ".join(authors) if authors else "Unknown"
        return BookModel(title=title, author=author, isbn=norm)
    except ValueError as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))


