from fastapi.testclient import TestClient
from fastapi import status

from api import app, lib

client = TestClient(app)


def test_books_crud_flow(monkeypatch, tmp_path):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    # stub add_book_by_isbn to avoid external call
    def fake_add(isbn, client_obj):
        from library import Book
        book = Book(title="Test", author="Yazar", isbn=isbn)
        lib.add_book(book)
        return book

    monkeypatch.setattr(type(lib), "add_book_by_isbn", lambda self, isbn, client: fake_add(isbn, client))

    # create
    resp = client.post("/books", json={"isbn": "111"})
    assert resp.status_code == status.HTTP_201_CREATED

    # list
    resp = client.get("/books")
    assert resp.status_code == 200
    data = resp.json()
    assert any(item["isbn"] == "111" for item in data)

    # delete
    resp = client.delete("/books/111")
    assert resp.status_code == status.HTTP_204_NO_CONTENT