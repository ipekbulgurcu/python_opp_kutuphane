from fastapi.testclient import TestClient
import types

from api import app, lib


client = TestClient(app)


def test_api_list_books_initial(tmp_path, monkeypatch):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    resp = client.get("/books")
    assert resp.status_code == 200
    assert resp.json() == []


def test_api_create_and_delete(monkeypatch, tmp_path):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    # stub OpenLibraryClient inside library by monkeypatching method on lib
    def fake_add(isbn, client_obj):
        from library import Book
        book = Book(title="Fake", author="Author", isbn=isbn)
        lib.add_book(book)
        return book

    monkeypatch.setattr(type(lib), "add_book_by_isbn", lambda self, isbn, client: fake_add(isbn, client))

    # create
    resp = client.post("/books", json={"isbn": "1234567890"})
    assert resp.status_code == 201
    data = resp.json()
    assert data["isbn"] == "1234567890"

    # delete
    resp = client.delete(f"/books/{data['isbn']}")
    assert resp.status_code == 204


