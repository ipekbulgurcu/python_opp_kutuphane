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


