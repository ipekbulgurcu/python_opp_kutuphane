# 📚 Python OOP Kütüphane Uygulaması

Bu proje, **Python ile Nesne Yönelimli Programlama** mantığını kullanarak hazırlanmış basit bir **kütüphane yönetim uygulamasıdır**. Uygulama hem terminal üzerinden (CLI) hem de **FastAPI tabanlı REST API** üzerinden kullanılabilir. Ayrıca FastAPI tarafından sunulan basit bir **HTML arayüzü** ve **Pytest ile yazılmış testler** bulunmaktadır.

---

## 🚀 Özellikler
- 📖 Kitap ekleme, listeleme ve silme işlemleri  
- 📂 JSON dosyası üzerinden kalıcı veri saklama  
- 🌐 FastAPI tabanlı UI desteği  
- 🖥️ Basit HTML kullanıcı arayüzü  
- ✅ Pytest ile test edilmiş modüller  
<img width="2875" height="1403" alt="ui_library" src="https://github.com/user-attachments/assets/4ffeacfb-17ad-4320-9651-a75d440121cd" />

---

## 🔧 Gereksinimler
- Python 3.9 veya üzeri  
- Gerekli bağımlılıkları yüklemek için:
```bash
pip install -r requirements.txt



## Proje Yapısı
python_opp_kutuphane/
├── api.py             # FastAPI uygulaması
├── library.py         # OOP sınıfları (Book, Library)
├── main.py            # CLI uygulaması
├── open_library.py    # Open Library API entegrasyonu
├── run_api.py         # API başlatma betiği
├── library.json       # Kitap verilerinin saklandığı dosya
├── ui/index.html      # Basit HTML arayüz
├── tests/             # Pytest test dosyaları
├── requirements.txt   # Bağımlılıklar
└── API_KULLANIM_KILAVUZU.md


## CLI Çalıştırma
```bash
python main.py
```
- Veriler aynı klasördeki `library.json` dosyasında kalıcıdır.

## API Çalıştırma
```bash
uvicorn api:app --reload
```
- Ana sayfa (HTML UI): http://127.0.0.1:8000/
- Swagger UI: http://127.0.0.1:8000/docs<img width="2878" height="1405" alt="barcode reader" src="https://github.com/user-attachments/assets/45ada6fc-0ec3-4ac8-a6bf-5f217e21e0e9" />

- Health Check: http://127.0.0.1:8000/health

### Endpointler
- GET `/books` → Tüm kitapları listeler
- POST `/books` → ISBN ile kitap ekle: `{ "isbn": "9789754341966" }` (Open Library’den başlık/yazar alınır)
- DELETE `/books/{isbn}` → ISBN’e göre siler (Tek bir kitabı sil)
- DELETE `/books` → Gövde: `{ "isbns": ["...", "..."] }` toplu (Birden fazla kitabı toplu sil)

### Testler
```bash
python -m pytest -q tests

-test_library.py: OOP yapısını test eder
-test_api_endpoints.py: API endpointlerini test eder
-test_main.py: CLI işlevlerini test eder
```
📖 Özet

Bu proje, Python OOP mantığıyla hazırlanmış bir kütüphane yönetim sistemi sunar. Hem CLI hem API üzerinden kullanılabilir, JSON tabanlı kalıcı veri saklar ve testlerle desteklenmiştir. Yazılım geliştirme öğrenenler için hem nesne yönelimli programlama, hem de API geliştirme konularında pratik bir örnek niteliği taşır.
---

<img width="2878" height="1405" alt="barcode reader" src="https://github.com/user-attachments/assets/05958e33-e04c-4c2a-845f-beab8c4839c3" />
