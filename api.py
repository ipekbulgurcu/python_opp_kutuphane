"""FastAPI uygulaması (Aşama 3)
GET /books, POST /books, DELETE /books/{isbn}
"""

from __future__ import annotations

from fastapi import FastAPI, HTTPException, status
from fastapi.responses import FileResponse
from pydantic import BaseModel
from pathlib import Path

from library import Library, Book
from open_library import OpenLibraryClient


app = FastAPI(title="Library API", version="1.0.0")
lib = Library()
client = OpenLibraryClient()

BASE_DIR = Path(__file__).resolve().parent
UI_INDEX = BASE_DIR / "ui" / "index.html"


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


class ISBNBody(BaseModel):
    isbn: str


@app.get("/books", response_model=list[BookModel])
def list_books():
    return [BookModel(title=b.title, author=b.author, isbn=b.isbn) for b in lib.list_books()]


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
    not_found: list[str] = []
    deleted: list[str] = []
    for isbn in body.isbns:
        if lib.remove_book(isbn):
            deleted.append(isbn)
        else:
            not_found.append(isbn)
    return {"deleted": deleted, "not_found": not_found}


