# 📚 Kütüphane Yönetim Sistemi API - Kullanım Kılavuzu

## 🚀 Hızlı Başlangıç

### 1. Gereksinimler
```bash
pip install -r requirements.txt
```

### 2. API'yi Başlatma
```bash
python run_api.py
```

### 3. API Dokümantasyonuna Erişim
API başlatıldıktan sonra aşağıdaki URL'lerden dokümantasyona erişebilirsiniz:

- **🌐 Ana Sayfa**: http://127.0.0.1:8000/
- **📚 Swagger UI**: http://127.0.0.1:8000/docs
- **📋 ReDoc**: http://127.0.0.1:8000/redoc
- **💚 Sağlık Kontrolü**: http://127.0.0.1:8000/health

## 📖 API Endpoint'leri

### 🏠 Ana Endpoint'ler
- `GET /` - Ana sayfa ve API bilgileri
- `GET /health` - Sağlık kontrolü
- `GET /slow-endpoint` - Asenkron işlem demosu

### 📚 Kitap İşlemleri
- `GET /books/` - Kitapları listele (sayfalama ile)
- `POST /books/` - Yeni kitap ekle
- `GET /books/{id}` - Kitap detayı
- `PUT /books/{id}` - Kitap güncelle
- `DELETE /books/{id}` - Kitap sil

### 🔒 Güvenli Endpoint'ler
- `GET /secure` - API Key test endpoint'i
- `GET /secure/books` - Güvenli kitap listesi

**API Key**: `SECRET_API_KEY_12345`  
**Header**: `X-API-Key: SECRET_API_KEY_12345`

### ⚡ Rate Limited Endpoint'ler
- `GET /limited` - 5 istek/dakika
- `GET /limited-strict` - 2 istek/dakika
- `GET /limited-books` - 10 istek/dakika

### 🌐 API Versioning
- `GET /api/v1/books` - v1 kitap listesi
- `GET /api/v2/books` - v2 gelişmiş kitap listesi

### 🔔 Background Tasks
- `POST /send-notification/{email}` - E-posta bildirimi

### 🔄 Demo Endpoint'ler
- `GET /error-demo` - Hata handling demosu

## 🧪 API Test Etme

### Otomatik Test
```bash
python test_api_endpoints.py
```

### Manuel Test (curl)
```bash
# Kitap listesi
curl http://127.0.0.1:8000/books/

# Yeni kitap ekleme
curl -X POST http://127.0.0.1:8000/books/ \
  -H "Content-Type: application/json" \
  -d '{"title": "Test Kitabı", "author": "Test Yazarı", "publication_year": 2024}'

# Güvenli endpoint (API Key ile)
curl -H "X-API-Key: SECRET_API_KEY_12345" http://127.0.0.1:8000/secure
```

## 📊 Swagger UI Özellikleri

Swagger UI (`/docs`) üzerinden:

✅ **Tüm endpoint'leri görüntüleme**  
✅ **Interactive testing** - Doğrudan tarayıcıdan test  
✅ **Request/Response örnekleri**  
✅ **Model şemaları** ve validasyon kuralları  
✅ **Authentication** test etme  
✅ **Rate limiting** görme  
✅ **Error handling** örnekleri  

## 🎯 Örnek Kullanım Senaryoları

### 1. Yeni Kitap Ekleme
1. Swagger UI'da `/books/` POST endpoint'ini açın
2. "Try it out" butonuna tıklayın
3. Örnek veriyi doldurun:
   ```json
   {
     "title": "1984",
     "author": "George Orwell",
     "publication_year": 1949
   }
   ```
4. "Execute" butonuna tıklayın

### 2. Güvenli Endpoint Test
1. `/secure` GET endpoint'ini açın
2. "Try it out" butonuna tıklayın
3. "Authorize" butonuna tıklayın (üst kısımda)
4. API Key girin: `SECRET_API_KEY_12345`
5. "Execute" butonuna tıklayın

### 3. Rate Limiting Test
1. `/limited` endpoint'ini açın
2. Peş peşe 6 kez "Execute" butonuna tıklayın
3. 6. istekte 429 hatası alacaksınız

## 🔧 Konfigürasyon

### Port Değiştirme
`run_api.py` dosyasında port değiştirebilirsiniz:
```python
uvicorn.run(..., port=8080, ...)
```

### API Key Değiştirme
`fastapi_main.py` dosyasında:
```python
API_KEY = "YENİ_API_KEY"
```

## 📝 Loglar

- **Uygulama logları**: Konsola yazdırılır
- **Bildirim logları**: `log.txt` dosyasına yazılır
- **Access logları**: Uvicorn tarafından gösterilir

## ❗ Sorun Giderme

### API başlamıyor
```bash
# Gereksinimler eksikse
pip install -r requirements.txt

# Port zaten kullanılıyorsa
lsof -ti:8000 | xargs kill -9  # macOS/Linux
netstat -ano | findstr :8000   # Windows
```

### Swagger UI açılmıyor
- http://127.0.0.1:8000/docs adresini kontrol edin
- API'nin tamamen başladığından emin olun
- Tarayıcı cache'ini temizleyin

### Rate limit hataları
- Dakika bekleyin veya API'yi yeniden başlatın

## 🎉 Özellikler

✨ **Modern FastAPI** - Async/await desteği  
📚 **Kapsamlı Swagger UI** - Interactive documentation  
🔒 **API Key Authentication** - Güvenli endpoint'ler  
⚡ **Rate Limiting** - İstek sınırlaması  
🌐 **API Versioning** - v1/v2 desteği  
🔄 **Background Tasks** - Asenkron işlemler  
📊 **Comprehensive Logging** - Detaylı loglar  
🧪 **Test Coverage** - Otomatik test desteği  

---

**🚀 API'nizi başlatın ve http://127.0.0.1:8000/docs adresinden şık Swagger UI dokümantasyonunu keşfedin!**
