# Kütüphane Uygulaması (CLI + FastAPI)

English version is below.

## Genel Bakış (TR)
Basit bir kütüphane uygulaması. Aşağıdakileri içerir:
- Python ile Nesne Yönelimli Programlama (CLI)
- JSON kalıcılık ile FastAPI backend
- FastAPI tarafından servis edilen basit HTML arayüz
- Pytest tabanlı testler

## Gereksinimler
- Python 3.9+

Bağımlılıkları kurun:
```bash
pip install -r python_oop_kutuphane/requirements.txt
```

## Proje Yapısı
- `python_oop_kutuphane/library.py`: OOP alanı (`Book`, `Library`)
- `python_oop_kutuphane/open_library.py`: Open Library istemcisi (httpx)
- `python_oop_kutuphane/main.py`: CLI uygulaması
- `python_oop_kutuphane/api.py`: FastAPI uygulaması
- `python_oop_kutuphane/ui/index.html`: Basit HTML arayüz
- `python_oop_kutuphane/tests/`: Pytest testleri

## CLI Çalıştırma
```bash
cd python_oop_kutuphane
python main.py
```
- Veriler aynı klasördeki `library.json` dosyasında kalıcıdır.

## API Çalıştırma
```bash
cd python_oop_kutuphane
uvicorn api:app --reload
```
- Ana sayfa (HTML UI): http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- Sağlık: http://127.0.0.1:8000/health

### Endpointler
- GET `/books` → Tüm kitapları listeler
- POST `/books` → Gövde: `{ "isbn": "9789754341966" }` (Open Library’den başlık/yazar alınır)
- DELETE `/books/{isbn}` → ISBN’e göre siler
- DELETE `/books` → Gövde: `{ "isbns": ["...", "..."] }` toplu silme

### Testler
```bash
cd python_oop_kutuphane
python -m pytest -q tests
```

---

# Library App (CLI + FastAPI)

## Overview (EN)
A simple library application including:
- Object-Oriented Programming in Python (CLI)
- A FastAPI backend with JSON persistence
- A minimal HTML UI served by FastAPI
- Pytest-based tests

## Requirements
- Python 3.9+

Install dependencies:
```bash
pip install -r python_oop_kutuphane/requirements.txt
```

## Project Structure
- `python_oop_kutuphane/library.py`: OOP domain (`Book`, `Library`)
- `python_oop_kutuphane/open_library.py`: Open Library client (httpx)
- `python_oop_kutuphane/main.py`: CLI app
- `python_oop_kutuphane/api.py`: FastAPI app
- `python_oop_kutuphane/ui/index.html`: Simple HTML UI
- `python_oop_kutuphane/tests/`: Pytest tests

## Run CLI
```bash
cd python_oop_kutuphane
python main.py
```
- Data is persisted to `library.json` in the same folder.

## Run API
```bash
cd python_oop_kutuphane
uvicorn api:app --reload
```
- Home (HTML UI): http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs
- Health: http://127.0.0.1:8000/health

### Endpoints
- GET `/books` → List all books
- POST `/books` → Body: `{ "isbn": "9789754341966" }` (fetches title/author from Open Library)
- DELETE `/books/{isbn}` → Delete by ISBN
- DELETE `/books` → Body: `{ "isbns": ["...", "..."] }` bulk delete

### Tests
```bash
cd python_oop_kutuphane
python -m pytest -q tests
```
