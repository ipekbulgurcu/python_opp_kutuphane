"""
OOP Kütüphane Uygulaması (Aşama 1 ve 2 gereksinimleri)
- JSON dosyasında kalıcı saklama
- ISBN ile Open Library API'den veri çekerek ekleme
"""

from __future__ import annotations

import json
import os
from dataclasses import dataclass, asdict
from typing import List, Optional, Tuple
from storage import Storage, JsonFileStorage


@dataclass
class LibraryItem:
    title: str
    author: str


@dataclass
class Book(LibraryItem):
    isbn: str

    def __str__(self) -> str:
        return f"{self.title} by {self.author} (ISBN: {self.isbn})"


class Library:
    def __init__(self, storage_path: str = "library.json", storage: Optional[Storage] = None):
        self.storage_path = storage_path
        self.storage: Storage = storage or JsonFileStorage(storage_path)
        self._books: List[Book] = []
        self.load_books()

    # Aşama 1
    def add_book(self, book: Book) -> None:
        if self.find_book(book.isbn):
            raise ValueError(f"Book with ISBN {book.isbn} already exists")
        self._books.append(book)
        self.save_books()

    def remove_book(self, isbn: str) -> bool:
        for i, b in enumerate(self._books):
            if b.isbn == isbn:
                self._books.pop(i)
                self.save_books()
                return True
        return False

    def remove_books(self, isbns: List[str]) -> Tuple[List[str], List[str]]:
        """Remove multiple books by ISBN. Returns (deleted, not_found)."""
        deleted: List[str] = []
        not_found: List[str] = []
        for isbn in isbns:
            if self.remove_book(isbn):
                deleted.append(isbn)
            else:
                not_found.append(isbn)
        return deleted, not_found

    def list_books(self) -> List[Book]:
        return list(self._books)

    def find_book(self, isbn: str) -> Optional[Book]:
        for b in self._books:
            if b.isbn == isbn:
                return b
        return None

    def load_books(self) -> None:
        raw = self.storage.read()
        self._books = [Book(**item) for item in raw]

    def save_books(self) -> None:
        data = [asdict(b) for b in self._books]
        self.storage.write(data)

    # Aşama 2
    def add_book_by_isbn(self, isbn: str, client: "OpenLibraryClient") -> Book:
        info = client.fetch_by_isbn(isbn)
        title = info["title"]
        authors: List[str] = info.get("authors", [])
        author = ", ".join(authors) if authors else "Unknown"
        book = Book(title=title, author=author, isbn=isbn)
        self.add_book(book)
        return book

    