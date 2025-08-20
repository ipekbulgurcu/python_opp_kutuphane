#!/usr/bin/env python3
"""
🚀 Kütüphane Yönetim API Başlatıcı
Bu script API'yi başlatır ve dokümantasyon URL'lerini gösterir.
"""

import uvicorn
import webbrowser
import time
import threading
from pathlib import Path

def print_banner():
    """API başlangıç banner'ını yazdırır."""
    print("=" * 60)
    print("📚 KÜTÜPHANE YÖNETİM SİSTEMİ API")
    print("=" * 60)
    print("🚀 API başlatılıyor...")
    print()

def print_urls():
    """Erişim URL'lerini yazdırır."""
    print("🌐 API Erişim URL'leri:")
    print("-" * 40)
    print("📖 Ana Sayfa:           http://127.0.0.1:8000/")
    print("📚 Swagger UI:          http://127.0.0.1:8000/docs")
    print("📋 ReDoc:               http://127.0.0.1:8000/redoc")
    print("🔧 OpenAPI JSON:        http://127.0.0.1:8000/openapi.json")
    print("💚 Sağlık Kontrolü:     http://127.0.0.1:8000/health")
    print()
    print("🔑 Güvenli endpoint'ler için API Key: SECRET_API_KEY_12345")
    print("📝 Header: X-API-Key: SECRET_API_KEY_12345")
    print()
    print("=" * 60)

def open_browser():
    """Tarayıcıda dokümantasyon sayfasını açar."""
    time.sleep(2)  # API'nin başlaması için bekle
    try:
        webbrowser.open("http://127.0.0.1:8000/docs")
        print("🌐 Tarayıcıda Swagger UI açıldı!")
    except Exception as e:
        print(f"⚠️  Tarayıcı açılamadı: {e}")

def main():
    """Ana fonksiyon."""
    print_banner()
    print_urls()
    
    # Tarayıcıyı arka planda aç
    browser_thread = threading.Thread(target=open_browser)
    browser_thread.daemon = True
    browser_thread.start()
    
    print("🔄 API çalışıyor... (Durdurmak için Ctrl+C)")
    print()
    
    try:
        # FastAPI uygulamasını başlat
        uvicorn.run(
            "fastapi_main:app",
            host="127.0.0.1",
            port=8000,
            reload=True,
            log_level="info",
            access_log=True
        )
    except KeyboardInterrupt:
        print("\n")
        print("👋 API kapatılıyor...")
        print("📚 Kütüphane Yönetim API başarıyla durduruldu!")

if __name__ == "__main__":
    main()
