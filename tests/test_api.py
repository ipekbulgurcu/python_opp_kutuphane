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
def test_api_preview_and_barcode_normalization(monkeypatch, tmp_path):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    # fake client response
    def fake_fetch(isbn: str):
        return {"title": "Fake", "authors": ["Author"]}

    monkeypatch.setattr("open_library.OpenLibraryClient.fetch_by_isbn", lambda self, isbn: fake_fetch(isbn))

    # EAN-13 (Bookland) barcode treated as ISBN-13
    resp = client.get("/books/preview/9781234567897")
    assert resp.status_code == 200
    assert resp.json()["title"] == "Fake"
    # normalized isbn should be returned (978... remains 978...)
    data = resp.json()
    assert data["isbn"] == "9781234567897"

    # delete
    resp = client.delete(f"/books/{data['isbn']}")
    assert resp.status_code == 404


def test_api_create_not_found(monkeypatch, tmp_path):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    # make add_book_by_isbn raise ValueError (simulating 404 from Open Library)
    def raise_not_found(self, isbn, client):
        raise ValueError("Kitap bulunamadı")

    monkeypatch.setattr(type(lib), "add_book_by_isbn", raise_not_found)

    resp = client.post("/books", json={"isbn": "0000000000"})
    assert resp.status_code == 404
    assert resp.json()["detail"] == "Kitap bulunamadı"


def test_api_create_network_error(monkeypatch, tmp_path):
    # isolate storage
    lib.storage_path = str(tmp_path / "library.json")
    lib._books = []
    lib.save_books()

    # make add_book_by_isbn raise a generic exception (simulating network/runtime error)
    def raise_runtime(self, isbn, client):
        raise RuntimeError("Ağ hatası: timeout")

    monkeypatch.setattr(type(lib), "add_book_by_isbn", raise_runtime)

    resp = client.post("/books", json={"isbn": "0000000000"})
    assert resp.status_code == 400
    assert "Ağ hatası" in resp.json()["detail"]

