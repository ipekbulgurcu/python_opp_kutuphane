from library import Library, Book


def test_add_list_remove_find(tmp_path):
    storage = tmp_path / "library.json"
    lib = Library(storage_path=str(storage))

    # initially empty
    assert lib.list_books() == []

    # add
    b = Book(title="Ulysses", author="James Joyce", isbn="9780199535675")
    lib.add_book(b)
    assert len(lib.list_books()) == 1
    assert lib.find_book(b.isbn) is not None

    # persist
    lib2 = Library(storage_path=str(storage))
    assert len(lib2.list_books()) == 1

    # remove
    assert lib2.remove_book(b.isbn) is True
    assert lib2.find_book(b.isbn) is None


def test_bulk_remove(tmp_path):
    storage = tmp_path / "library.json"
    lib = Library(storage_path=str(storage))

    b1 = Book(title="A", author="AA", isbn="1")
    b2 = Book(title="B", author="BB", isbn="2")
    b3 = Book(title="C", author="CC", isbn="3")
    lib.add_book(b1)
    lib.add_book(b2)
    lib.add_book(b3)

    deleted, not_found = lib.remove_books(["1", "4", "3"])  # 2 kitap var, 1 tanesi yok
    assert set(deleted) == {"1", "3"}
    assert set(not_found) == {"4"}
    assert lib.find_book("1") is None
    assert lib.find_book("3") is None
    assert lib.find_book("2") is not None


