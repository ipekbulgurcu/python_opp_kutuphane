#!/usr/bin/env python3
"""
🧪 API Endpoint Test Scripti
Bu script tüm API endpoint'lerini test eder.
"""

import httpx
import json
import time
from typing import Dict, Any

# API konfigürasyonu
BASE_URL = "http://127.0.0.1:8000"
API_KEY = "SECRET_API_KEY_12345"
HEADERS = {"X-API-Key": API_KEY}

def print_test_header(test_name: str):
    """Test başlığını yazdırır."""
    print(f"\n{'='*50}")
    print(f"🧪 TEST: {test_name}")
    print('='*50)

def print_response(response: httpx.Response):
    """HTTP yanıtını formatlar ve yazdırır."""
    print(f"📊 Status: {response.status_code}")
    print(f"⏱️  Süre: {response.elapsed.total_seconds():.3f}s")
    
    try:
        data = response.json()
        print(f"📄 Response:")
        print(json.dumps(data, indent=2, ensure_ascii=False))
    except:
        print(f"📄 Response: {response.text}")
    print("-" * 30)

def test_basic_endpoints():
    """Temel endpoint'leri test eder."""
    print_test_header("Temel Endpoint'ler")
    
    endpoints = [
        ("Ana Sayfa", "GET", "/"),
        ("Sağlık Kontrolü", "GET", "/health"),
        ("Yavaş Endpoint", "GET", "/slow-endpoint"),
    ]
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        for name, method, path in endpoints:
            print(f"🔍 Test: {name} ({method} {path})")
            try:
                response = client.request(method, path)
                print_response(response)
            except Exception as e:
                print(f"❌ Hata: {e}")

def test_book_crud():
    """Kitap CRUD işlemlerini test eder."""
    print_test_header("Kitap CRUD İşlemleri")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        # 1. Kitapları listele
        print("🔍 Test: Kitapları Listele")
        response = client.get("/books/")
        print_response(response)
        
        # 2. Yeni kitap ekle
        print("🔍 Test: Yeni Kitap Ekle")
        new_book = {
            "title": "Test Kitabı",
            "author": "Test Yazarı",
            "publication_year": 2024
        }
        response = client.post("/books/", json=new_book)
        print_response(response)
        
        if response.status_code == 201:
            book_data = response.json()
            book_id = book_data["id"]
            
            # 3. Kitap detayını getir
            print(f"🔍 Test: Kitap Detayı Getir (ID: {book_id})")
            response = client.get(f"/books/{book_id}")
            print_response(response)
            
            # 4. Kitabı güncelle
            print(f"🔍 Test: Kitap Güncelle (ID: {book_id})")
            updated_book = {
                "title": "Güncellenmiş Test Kitabı",
                "author": "Güncellenmiş Test Yazarı",
                "publication_year": 2024
            }
            response = client.put(f"/books/{book_id}", json=updated_book)
            print_response(response)
            
            # 5. Kitabı sil
            print(f"🔍 Test: Kitap Sil (ID: {book_id})")
            response = client.delete(f"/books/{book_id}")
            print_response(response)

def test_security_endpoints():
    """Güvenlik endpoint'lerini test eder."""
    print_test_header("Güvenlik Endpoint'leri")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        # API Key olmadan
        print("🔍 Test: Güvenli Endpoint (API Key Yok)")
        response = client.get("/secure")
        print_response(response)
        
        # API Key ile
        print("🔍 Test: Güvenli Endpoint (API Key Var)")
        response = client.get("/secure", headers=HEADERS)
        print_response(response)
        
        # Güvenli kitap listesi
        print("🔍 Test: Güvenli Kitap Listesi")
        response = client.get("/secure/books", headers=HEADERS)
        print_response(response)

def test_rate_limiting():
    """Rate limiting'i test eder."""
    print_test_header("Rate Limiting")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        # Normal rate limit test
        print("🔍 Test: Rate Limited Endpoint (5 istek)")
        for i in range(6):  # 5'ten fazla istek gönder
            print(f"İstek {i+1}/6")
            response = client.get("/limited")
            print(f"Status: {response.status_code}")
            if response.status_code == 429:
                print("✅ Rate limit çalışıyor!")
                break
            time.sleep(0.1)

def test_versioning():
    """API versioning'i test eder."""
    print_test_header("API Versioning")
    
    endpoints = [
        ("API v1", "GET", "/api/v1/books"),
        ("API v2", "GET", "/api/v2/books"),
    ]
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        for name, method, path in endpoints:
            print(f"🔍 Test: {name} ({method} {path})")
            try:
                response = client.request(method, path)
                print_response(response)
            except Exception as e:
                print(f"❌ Hata: {e}")

def test_background_tasks():
    """Background task'ları test eder."""
    print_test_header("Background Tasks")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        print("🔍 Test: E-posta Bildirimi Gönder")
        response = client.post("/send-notification/test@example.com?message=Test%20mesajı")
        print_response(response)

def test_error_handling():
    """Hata handling'i test eder."""
    print_test_header("Hata Handling")
    
    with httpx.Client(base_url=BASE_URL, timeout=30.0) as client:
        print("🔍 Test: Hata Demo")
        response = client.get("/error-demo")
        print_response(response)
        
        print("🔍 Test: Olmayan Kitap")
        response = client.get("/books/999999")
        print_response(response)

def main():
    """Ana test fonksiyonu."""
    print("🚀 API Endpoint Test Scripti Başlatılıyor...")
    print(f"📡 Base URL: {BASE_URL}")
    print(f"🔑 API Key: {API_KEY}")
    
    try:
        # API'nin hazır olduğunu kontrol et
        with httpx.Client(base_url=BASE_URL, timeout=5.0) as client:
            response = client.get("/health")
            if response.status_code != 200:
                print("❌ API hazır değil! Önce API'yi başlatın.")
                return
        
        print("✅ API hazır, testler başlıyor...\n")
        
        # Tüm testleri çalıştır
        test_basic_endpoints()
        test_book_crud()
        test_security_endpoints()
        test_rate_limiting()
        test_versioning()
        test_background_tasks()
        test_error_handling()
        
        print("\n" + "="*60)
        print("🎉 Tüm testler tamamlandı!")
        print("📚 Swagger UI: http://127.0.0.1:8000/docs")
        print("="*60)
        
    except httpx.ConnectError:
        print("❌ API'ye bağlanılamıyor!")
        print("💡 Önce 'python run_api.py' komutu ile API'yi başlatın.")
    except Exception as e:
        print(f"❌ Beklenmeyen hata: {e}")

if __name__ == "__main__":
    main()
