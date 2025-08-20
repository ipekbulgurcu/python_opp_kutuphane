"""
FastAPI ile Modern API Geliştirme - Kapsamlı Uygulama
Notebook içeriğine göre konsolide edilmiştir.
"""

import asyncio
import logging
from enum import IntEnum
from typing import Annotated, Optional, List
from contextlib import asynccontextmanager

from fastapi import (
    FastAPI,
    Body,
    Query,
    Path,
    Security,
    Depends,
    HTTPException,
    BackgroundTasks,
    status,
    Request,
)
from fastapi.security import APIKeyHeader
from pydantic import BaseModel, Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

# Logging configuration
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ===== Rate Limiter Configuration =====
limiter = Limiter(key_func=get_remote_address)

# ===== In-Memory Database (for demo purposes) =====
books_db: List[dict] = []
book_id_counter: int = 1

# ===== Lifespan Event Handler =====
@asynccontextmanager
async def lifespan(app: FastAPI):
    """Handle application startup and shutdown events."""
    logger.info("FastAPI application starting up...")

    # Add some sample data
    sample_books = [
        {"id": 1, "title": "The Hobbit", "author": "J.R.R. Tolkien", "publication_year": 1937},
        {"id": 2, "title": "1984", "author": "George Orwell", "publication_year": 1949},
        {"id": 3, "title": "Dune", "author": "Frank Herbert", "publication_year": 1965},
    ]

    books_db.extend(sample_books)
    global book_id_counter
    book_id_counter = 4

    logger.info(f"Loaded {len(sample_books)} sample books")

    yield  # Application runs here

    logger.info("FastAPI application shutting down...")

# FastAPI app instance with lifespan and enhanced documentation
app = FastAPI(
    title="📚 Kütüphane Yönetim Sistemi API",
    description="""
    ## Modern Kütüphane Yönetim Sistemi

    Bu API, kapsamlı kütüphane yönetimi için geliştirilmiş modern bir REST API'dir.

    ### 🚀 Özellikler

    * **📖 Kitap Yönetimi**: CRUD operasyonları ile kitap ekleme, güncelleme, silme ve listeleme
    * **🔒 Güvenlik**: API Key tabanlı authentication sistemi
    * **⚡ Rate Limiting**: Dakika başına istek sınırlaması
    * **📊 Versioning**: API versiyonlama desteği
    * **🔄 Async**: Asenkron işlemler ve background task desteği
    * **📝 Logging**: Kapsamlı log kayıt sistemi

    ### 🔐 Authentication

    Güvenli endpoint'ler için `X-API-Key` header'ı kullanın:
    ```
    X-API-Key: SECRET_API_KEY_12345
    ```

    ### 📈 Rate Limits

    - Genel endpoint'ler: 5 istek/dakika
    - Sıkı sınırlı endpoint'ler: 2 istek/dakika
    - Kitap endpoint'leri: 10 istek/dakika

    ### 🌐 API Versions

    - **v1**: Temel kitap listesi
    - **v2**: Gelişmiş kitap listesi (toplam sayı ile)

    ---
    **Geliştirici**: Python OOP Kütüphane Projesi  
    **Teknoloji**: FastAPI + Pydantic + Async/Await
    """,
    version="2.0.0",
    contact={
        "name": "API Desteği",
        "email": "destek@kutuphane.com",
    },
    license_info={
        "name": "MIT License",
        "url": "https://opensource.org/licenses/MIT",
    },
    servers=[
        {
            "url": "http://127.0.0.1:8000",
            "description": "Geliştirme Sunucusu"
        }
    ],
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Add rate limiter to app
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)

# ===== Pydantic Models =====
class Book(BaseModel):
    """📖 Kitap modeli - Kitap güncelleme işlemleri için kullanılır."""
    
    title: str = Field(
        ..., 
        min_length=3, 
        max_length=200,
        description="Kitap başlığı (en az 3, en fazla 200 karakter)",
        example="1984"
    )
    author: str = Field(
        ...,
        min_length=2,
        max_length=100, 
        description="Yazar adı (en az 2, en fazla 100 karakter)",
        example="George Orwell"
    )
    publication_year: Optional[int] = Field(
        default=None,
        gt=1400, 
        le=2024,
        description="Yayın yılı (1400-2024 arası)",
        example=1949
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "1984",
                "author": "George Orwell", 
                "publication_year": 1949
            }
        }

class BookCreate(BaseModel):
    """📝 Yeni kitap oluşturma modeli - Yeni kitap eklerken kullanılır."""
    
    title: str = Field(
        ..., 
        min_length=3,
        max_length=200,
        description="Kitap başlığı (en az 3, en fazla 200 karakter)",
        example="Dune"
    )
    author: str = Field(
        ...,
        min_length=2,
        max_length=100,
        description="Yazar adı (en az 2, en fazla 100 karakter)",
        example="Frank Herbert"
    )
    publication_year: Optional[int] = Field(
        default=None,
        gt=1400,
        le=2024,
        description="Yayın yılı (1400-2024 arası, opsiyonel)",
        example=1965
    )

    class Config:
        json_schema_extra = {
            "example": {
                "title": "Dune",
                "author": "Frank Herbert",
                "publication_year": 1965
            }
        }

class BookResponse(BaseModel):
    """📚 Kitap yanıt modeli - API'den dönen kitap bilgileri."""
    
    id: int = Field(
        ...,
        description="Benzersiz kitap ID'si",
        example=1
    )
    title: str = Field(
        ...,
        description="Kitap başlığı",
        example="The Hobbit"
    )
    author: str = Field(
        ...,
        description="Yazar adı",
        example="J.R.R. Tolkien"
    )
    publication_year: Optional[int] = Field(
        default=None,
        description="Yayın yılı",
        example=1937
    )

    class Config:
        json_schema_extra = {
            "example": {
                "id": 1,
                "title": "The Hobbit",
                "author": "J.R.R. Tolkien",
                "publication_year": 1937
            }
        }

# ===== HTTP Status Codes =====
class HTTPStatusCodes(IntEnum):
    OK = 200
    CREATED = 201
    NO_CONTENT = 204
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    UNPROCESSABLE_ENTITY = 422

# ===== Security Configuration =====
API_KEY = "SECRET_API_KEY_12345"
API_KEY_NAME = "X-API-Key"
api_key_header = APIKeyHeader(name=API_KEY_NAME, auto_error=False)

async def get_api_key(api_key: str = Security(api_key_header)):
    if api_key == API_KEY:
        return api_key
    raise HTTPException(
        status_code=status.HTTP_403_FORBIDDEN,
        detail="Could not validate credentials",
    )

# ===== Async Helper Functions =====
async def slow_db_call():
    await asyncio.sleep(1)
    return {"status": "done"}

# ===== Background Task Functions =====
def write_notification(email: str, message: str = ""):
    try:
        with open("log.txt", mode="a", encoding="utf-8") as email_file:
            content = f"notification for {email}: {message}\n"
            email_file.write(content)
        logger.info(f"Notification written for {email}")
    except Exception as e:
        logger.error(f"Failed to write notification: {e}")

# ===== API Endpoints =====
@app.get(
    "/",
    tags=["🏠 Ana Sayfa"],
    summary="Ana Sayfa",
    description="API'nin ana sayfası - mevcut endpoint'leri ve temel bilgileri gösterir."
)
async def root():
    """
    🏠 **Ana Sayfa Endpoint'i**
    
    Bu endpoint API'nin çalıştığını doğrular ve mevcut endpoint'ler hakkında bilgi verir.
    """
    return {
        "message": "📚 Kütüphane Yönetim Sistemi API'sine Hoş Geldiniz!",
        "version": "2.0.0",
        "documentation": "/docs",
        "alternative_docs": "/redoc",
        "endpoints": {
            "books": "/books",
            "health": "/health",
            "secure": "/secure"
        }
    }

@app.get(
    "/health",
    tags=["🔧 Sistem"],
    summary="Sağlık Kontrolü",
    description="API'nin sağlık durumunu kontrol eder."
)
async def health_check():
    """
    🔧 **Sağlık Kontrolü Endpoint'i**
    
    Bu endpoint API'nin çalışır durumda olduğunu kontrol etmek için kullanılır.
    Monitoring ve health check sistemleri için idealdir.
    """
    return {
        "status": "healthy",
        "timestamp": "2024-01-01T00:00:00Z",
        "service": "Library Management API",
        "version": "2.0.0"
    }

# ===== Demo Endpoints =====
@app.get(
    "/slow-endpoint",
    tags=["🔄 Demo"],
    summary="Yavaş İşlem Demosu",
    description="Asenkron işlemleri göstermek için 1 saniye bekleyen demo endpoint."
)
async def handle_slow_request():
    """
    🔄 **Asenkron İşlem Demosu**
    
    Bu endpoint asenkron işlemlerin nasıl çalıştığını gösterir.
    1 saniye bekler ve sonuç döner.
    """
    logger.info("İstek alındı, yavaş işlem bekleniyor...")
    result = await slow_db_call()
    logger.info("Yavaş işlem tamamlandı, yanıt gönderiliyor.")
    return result

# ===== Kitap CRUD İşlemleri =====
@app.post(
    "/books/",
    response_model=BookResponse,
    status_code=status.HTTP_201_CREATED,
    tags=["📚 Kitap İşlemleri"],
    summary="Yeni Kitap Ekle",
    description="Kütüphaneye yeni bir kitap ekler."
)
async def create_book(book: BookCreate):
    """
    📝 **Yeni Kitap Ekleme**
    
    Bu endpoint kütüphaneye yeni bir kitap ekler.
    
    **Parametreler:**
    - **title**: Kitap başlığı (zorunlu, 3-200 karakter)
    - **author**: Yazar adı (zorunlu, 2-100 karakter)
    - **publication_year**: Yayın yılı (opsiyonel, 1400-2024 arası)
    
    **Dönen Değer:**
    Eklenen kitabın bilgileri ve otomatik atanan ID.
    """
    global book_id_counter
    new_book = BookResponse(
        id=book_id_counter,
        title=book.title,
        author=book.author,
        publication_year=book.publication_year,
    )
    books_db.append(new_book.model_dump())
    book_id_counter += 1
    logger.info(f"Created book: {new_book.title}")
    return new_book

@app.get(
    "/books/",
    response_model=List[BookResponse],
    tags=["📚 Kitap İşlemleri"],
    summary="Kitapları Listele",
    description="Kütüphanedeki kitapları sayfalama ile listeler."
)
async def list_books(
    skip: Annotated[int, Query(description="Atlanacak kitap sayısı", ge=0)] = 0,
    limit: Annotated[int, Query(description="Getirilecek kitap sayısı", ge=1, le=100)] = 10,
):
    """
    📖 **Kitap Listeleme**
    
    Bu endpoint kütüphanedeki kitapları sayfalama ile listeler.
    
    **Query Parametreleri:**
    - **skip**: Atlanacak kitap sayısı (varsayılan: 0)
    - **limit**: Getirilecek kitap sayısı (1-100 arası, varsayılan: 10)
    
    **Dönen Değer:**
    Belirtilen aralıktaki kitapların listesi.
    """
    return books_db[skip : skip + limit]

@app.get(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["📚 Kitap İşlemleri"],
    summary="Kitap Detayı",
    description="Belirtilen ID'ye sahip kitabın detaylarını getirir."
)
async def get_book(book_id: Annotated[int, Path(title="Kitap ID'si", ge=1, description="Getirilecek kitabın benzersiz ID'si")]):
    """
    🔍 **Kitap Detayı Getirme**
    
    Bu endpoint belirtilen ID'ye sahip kitabın detaylarını getirir.
    
    **Path Parametresi:**
    - **book_id**: Kitabın benzersiz ID'si (pozitif tam sayı)
    
    **Dönen Değer:**
    Kitabın tüm bilgileri (ID, başlık, yazar, yayın yılı).
    
    **Hata Durumları:**
    - 404: Belirtilen ID'ye sahip kitap bulunamadı
    """
    for book in books_db:
        if book["id"] == book_id:
            return book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"ID {book_id} olan kitap bulunamadı"
    )

@app.put(
    "/books/{book_id}",
    response_model=BookResponse,
    tags=["📚 Kitap İşlemleri"],
    summary="Kitap Güncelle",
    description="Belirtilen ID'ye sahip kitabın bilgilerini günceller."
)
async def update_book(
    book_id: Annotated[int, Path(title="Kitap ID'si", ge=1, description="Güncellenecek kitabın ID'si")],
    book: Book,
    version: Annotated[Optional[int], Query(title="Versiyon Numarası", ge=1, description="Optimistic locking için versiyon")] = None,
):
    """
    ✏️ **Kitap Güncelleme**
    
    Bu endpoint mevcut bir kitabın bilgilerini günceller.
    
    **Path Parametresi:**
    - **book_id**: Güncellenecek kitabın benzersiz ID'si
    
    **Query Parametresi:**
    - **version**: Optimistic locking için versiyon numarası (opsiyonel)
    
    **Request Body:**
    Güncellenecek kitap bilgileri (title, author, publication_year)
    
    **Dönen Değer:**
    Güncellenen kitabın yeni bilgileri.
    
    **Hata Durumları:**
    - 404: Belirtilen ID'ye sahip kitap bulunamadı
    - 422: Geçersiz veri formatı
    """
    for i, existing_book in enumerate(books_db):
        if existing_book["id"] == book_id:
            updated_book = {
                "id": book_id,
                "title": book.title,
                "author": book.author,
                "publication_year": book.publication_year,
            }
            books_db[i] = updated_book
            logger.info(f"Updated book {book_id}, version: {version}")
            return updated_book
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"ID {book_id} olan kitap bulunamadı"
    )

@app.delete(
    "/books/{book_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    tags=["📚 Kitap İşlemleri"],
    summary="Kitap Sil",
    description="Belirtilen ID'ye sahip kitabı kütüphaneden siler."
)
async def delete_book(book_id: Annotated[int, Path(title="Kitap ID'si", ge=1, description="Silinecek kitabın ID'si")]):
    """
    🗑️ **Kitap Silme**
    
    Bu endpoint belirtilen ID'ye sahip kitabı kütüphaneden kalıcı olarak siler.
    
    **Path Parametresi:**
    - **book_id**: Silinecek kitabın benzersiz ID'si
    
    **Dönen Değer:**
    Başarılı silme işlemi için 204 No Content status kodu.
    
    **Hata Durumları:**
    - 404: Belirtilen ID'ye sahip kitap bulunamadı
    
    **⚠️ Uyarı:** Bu işlem geri alınamaz!
    """
    for i, book in enumerate(books_db):
        if book["id"] == book_id:
            deleted_book_title = book["title"]
            books_db.pop(i)
            logger.info(f"Deleted book with id {book_id}: {deleted_book_title}")
            return
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"ID {book_id} olan kitap bulunamadı"
    )

# ===== Güvenli Endpoint'ler =====
@app.get(
    "/secure",
    tags=["🔒 Güvenlik"],
    summary="Güvenli Endpoint Test",
    description="API Key authentication test endpoint'i."
)
async def secure_endpoint(api_key: str = Depends(get_api_key)):
    """
    🔒 **Güvenli Endpoint Test**
    
    Bu endpoint API Key authentication sistemini test etmek için kullanılır.
    
    **Authentication:**
    Header'da `X-API-Key: SECRET_API_KEY_12345` göndermeniz gerekir.
    
    **Dönen Değer:**
    Başarılı authentication durumunda onay mesajı.
    
    **Hata Durumları:**
    - 403: Geçersiz veya eksik API Key
    """
    return {
        "message": "🎉 Tebrikler! API anahtarınız geçerli ve güvenli endpoint'e erişim sağladınız.",
        "authenticated": True,
        "api_key_status": "valid"
    }

@app.get(
    "/secure/books",
    response_model=List[BookResponse],
    tags=["🔒 Güvenlik"],
    summary="Güvenli Kitap Listesi",
    description="API Key gerektiren kitap listesi endpoint'i."
)
async def secure_list_books(api_key: str = Depends(get_api_key)):
    """
    🔒📚 **Güvenli Kitap Listesi**
    
    Bu endpoint tüm kitapları listeler ancak API Key authentication gerektirir.
    
    **Authentication:**
    Header'da `X-API-Key: SECRET_API_KEY_12345` göndermeniz gerekir.
    
    **Dönen Değer:**
    Kütüphanedeki tüm kitapların listesi.
    
    **Hata Durumları:**
    - 403: Geçersiz veya eksik API Key
    """
    return books_db

# ===== Background Task Endpoint'leri =====
@app.post(
    "/send-notification/{email}",
    tags=["🔔 Bildirimler"],
    summary="E-posta Bildirimi Gönder",
    description="Belirtilen e-posta adresine background task ile bildirim gönderir."
)
async def send_notification(
    email: str = Path(..., description="Bildirim gönderilecek e-posta adresi"),
    background_tasks: BackgroundTasks = None,
    message: str = Query("Kitap bildirimi", description="Gönderilecek mesaj")
):
    """
    🔔 **Background Task ile E-posta Bildirimi**
    
    Bu endpoint belirtilen e-posta adresine background task ile bildirim gönderir.
    İstek hemen döner, bildirim arka planda işlenir.
    
    **Path Parametresi:**
    - **email**: Bildirim gönderilecek e-posta adresi
    
    **Query Parametresi:**
    - **message**: Gönderilecek mesaj (varsayılan: "Kitap bildirimi")
    
    **Dönen Değer:**
    Bildirimin arka planda gönderileceğine dair onay mesajı.
    
    **Not:** Bildirim log.txt dosyasına yazılır.
    """
    background_tasks.add_task(write_notification, email, message=message)
    return {
        "message": "📧 Bildirim arka planda gönderiliyor...",
        "email": email,
        "status": "queued"
    }

# ===== Rate Limited Endpoint'ler =====
@app.get(
    "/limited",
    tags=["⚡ Rate Limiting"],
    summary="Rate Limited Endpoint (5/dk)",
    description="Dakikada maksimum 5 istek kabul eden endpoint."
)
@limiter.limit("5/minute")
async def limited_endpoint(request: Request):
    """
    ⚡ **Rate Limited Endpoint (5/dakika)**
    
    Bu endpoint dakikada maksimum 5 istek kabul eder.
    Limit aşıldığında 429 Too Many Requests hatası döner.
    
    **Rate Limit:** 5 istek/dakika
    
    **Hata Durumları:**
    - 429: Rate limit aşıldı
    """
    return {
        "message": "✅ Bu endpoint dakikada maksimum 5 istek kabul eder.",
        "rate_limit": "5/minute",
        "status": "success"
    }

@app.get(
    "/limited-strict",
    tags=["⚡ Rate Limiting"],
    summary="Sıkı Rate Limited Endpoint (2/dk)",
    description="Dakikada maksimum 2 istek kabul eden sıkı endpoint."
)
@limiter.limit("2/minute")
async def strict_limited_endpoint(request: Request):
    """
    ⚡ **Sıkı Rate Limited Endpoint (2/dakika)**
    
    Bu endpoint dakikada maksimum 2 istek kabul eder.
    Çok sıkı rate limiting uygulanır.
    
    **Rate Limit:** 2 istek/dakika
    
    **Hata Durumları:**
    - 429: Rate limit aşıldı
    """
    return {
        "message": "✅ Bu endpoint dakikada maksimum 2 istek kabul eder.",
        "rate_limit": "2/minute",
        "status": "success",
        "warning": "Çok sıkı limit uygulanır!"
    }

@app.get(
    "/limited-books",
    tags=["⚡ Rate Limiting"],
    summary="Rate Limited Kitap Endpoint (10/dk)",
    description="Dakikada maksimum 10 istek kabul eden kitap bilgi endpoint'i."
)
@limiter.limit("10/minute")
async def rate_limited_books(request: Request):
    """
    ⚡📚 **Rate Limited Kitap Endpoint (10/dakika)**
    
    Bu endpoint kitap bilgilerini rate limit ile döner.
    Dakikada maksimum 10 istek kabul eder.
    
    **Rate Limit:** 10 istek/dakika
    
    **Dönen Değer:**
    - Toplam kitap sayısı
    - İlk 5 kitabın bilgileri
    
    **Hata Durumları:**
    - 429: Rate limit aşıldı
    """
    return {
        "message": "📚 Rate limited kitap endpoint'i",
        "total_books": len(books_db),
        "books_preview": books_db[:5],
        "rate_limit": "10/minute"
    }

# ===== API Versioning Endpoint'leri =====
@app.get(
    "/api/v1/books",
    response_model=list[BookResponse],
    tags=["🌐 API Versioning"],
    summary="Kitap Listesi v1",
    description="API v1 - Basit kitap listesi."
)
async def list_books_v1():
    """
    🌐 **API v1 - Kitap Listesi**
    
    Bu endpoint API'nin 1. versiyonudur.
    Basit kitap listesi döner.
    
    **Dönen Değer:**
    Tüm kitapların basit listesi.
    
    **Versiyon Özellikleri:**
    - Basit liste formatı
    - Metadata yok
    - Geriye uyumluluk garantisi
    """
    return books_db

@app.get(
    "/api/v2/books",
    tags=["🌐 API Versioning"],
    summary="Kitap Listesi v2",
    description="API v2 - Gelişmiş kitap listesi (metadata ile)."
)
async def list_books_v2():
    """
    🌐 **API v2 - Gelişmiş Kitap Listesi**
    
    Bu endpoint API'nin 2. versiyonudur.
    Kitap listesini metadata ile birlikte döner.
    
    **Dönen Değer:**
    - API versiyon bilgisi
    - Toplam kitap sayısı
    - Kitap listesi
    
    **Versiyon Özellikleri:**
    - Gelişmiş response formatı
    - Metadata dahil
    - Daha fazla bilgi
    """
    return {
        "version": "2.0",
        "api_info": {
            "title": "Kütüphane Yönetim API",
            "description": "Gelişmiş kitap listesi endpoint'i"
        },
        "total_books": len(books_db),
        "books": books_db,
        "metadata": {
            "response_time": "2024-01-01T00:00:00Z",
            "data_source": "in_memory_db"
        }
    }

# ===== Hata Handling Demo =====
@app.get(
    "/error-demo",
    tags=["🔄 Demo"],
    summary="Hata Handling Demosu",
    description="HTTP hata handling sistemini göstermek için demo endpoint."
)
async def error_demo():
    """
    🔄 **HTTP Hata Handling Demosu**
    
    Bu endpoint HTTP hata handling sistemini göstermek için
    kasıtlı olarak 400 Bad Request hatası fırlatır.
    
    **Dönen Değer:**
    Her zaman 400 Bad Request hatası.
    
    **Amaç:**
    - Error handling sistemini test etmek
    - HTTP status kodlarını göstermek
    - Exception handling'i örneklemek
    """
    raise HTTPException(
        status_code=status.HTTP_400_BAD_REQUEST,
        detail="🚨 Bu demo bir hata mesajıdır! Hata handling sistemi çalışıyor."
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("fastapi_main:app", host="127.0.0.1", port=8000, reload=True, log_level="info") 
