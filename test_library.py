from library import Book, Library


def test_book_str():
    b = Book("The Hobbit", "J.R.R. Tolkien", "9780345339683")
    s = str(b)
    assert "The Hobbit" in s and "J.R.R. Tolkien" in s and "9780345339683" in s


def test_persistence(tmp_path):
    storage = tmp_path / "library.json"
    lib = Library(storage_path=str(storage))
    assert lib.list_books() == []

    b = Book("Ulysses", "James Joyce", "9780199535675")
    lib.add_book(b)
    assert len(lib.list_books()) == 1

    lib2 = Library(storage_path=str(storage))
    assert len(lib2.list_books()) == 1