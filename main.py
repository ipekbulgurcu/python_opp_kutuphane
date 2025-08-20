"""Komut satırı uygulaması (Aşama 1 ve 2)
Menü tabanlı basit CLI.
"""

from __future__ import annotations

from library import Library
from open_library import OpenLibraryClient


def print_menu() -> None:
    print("\n--- Menü ---")
    print("1. Kitap Ekle (ISBN ile)")
    print("2. Kitap Sil")
    print("3. Kitapları Listele")
    print("4. Kitap Ara (ISBN)")
    print("5. Çoklu Sil (virgülle ISBN girin)")
    print("6. Çıkış")


def main() -> None:
    lib = Library()
    client = OpenLibraryClient()

    while True:
        print_menu()
        choice = input("Seçiminiz: ").strip()
        if choice == "1":
            isbn = input("ISBN: ").strip()
            try:
                book = lib.add_book_by_isbn(isbn, client)
                print(f"Eklendi: {book}")
            except Exception as e:
                print(f"Hata: {e}")
        elif choice == "2":
            isbn = input("Silinecek ISBN: ").strip()
            ok = lib.remove_book(isbn)
            print("Silindi" if ok else "Bulunamadı")
        elif choice == "3":
            for b in lib.list_books():
                print("-", b)
        elif choice == "4":
            isbn = input("ISBN: ").strip()
            b = lib.find_book(isbn)
            print(b if b else "Bulunamadı")
        elif choice == "5":
            raw = input("Silinecek ISBN'ler (virgülle): ").strip()
            isbns = [s.strip() for s in raw.split(",") if s.strip()]
            deleted, not_found = lib.remove_books(isbns)
            print(f"Silindi: {len(deleted)}, Bulunamadı: {len(not_found)}")
        elif choice == "6":
            print("Çıkılıyor...")
            break
        else:
            print("Geçersiz seçim")


if __name__ == "__main__":
    main()


