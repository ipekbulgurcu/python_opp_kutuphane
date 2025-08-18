import pytest # Pytest'i ve test edilecek sınıfı import et
from library import Book

def test_book_creation():
    """Test if a Book object is created with correct attributes."""
    # 1. Kur (Setup)
    book = Book("The Hobbit", "J.R.R. Tolkien", "978-0345339683")

    # 3. Doğrula (Assert)
    assert book.title == "The Hobbit"
    assert book.author == "J.R.R. Tolkien"
    assert book.is_borrowed == False

def test_borrow_and_return_logic():
    """Tests the core borrowing and returning functionality."""
    # 1. Kur (Setup)
    book = Book("Dune", "Frank Herbert", "978-0441013593")
    # 2. Harekete Geç (Action)
    book.borrow_book()
    # 3. Doğrula (Assert)
    assert book.is_borrowed == True

    # 2. Harekete Geç (Action)
    book.return_book()
    # 3. Doğrula (Assert)
    assert book.is_borrowed == False

# Terminalde 'pytest' komutunu çalıştırdığımızda bu testler otomatik olarak bulunur ve çalıştırılır.
# Yeşil renkli 'PASSED' çıktısı, kodumuzun beklediğimiz gibi çalıştığını gösterir.