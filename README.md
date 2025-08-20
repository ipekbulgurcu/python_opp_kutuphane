# 📚 Python OOP Kütüphane Uygulaması

Bu proje, **Python ile Nesne Yönelimli Programlama (OOP)** mantığı kullanılarak geliştirilmiş, basit ve işlevsel bir **kütüphane yönetim uygulamasıdır**. Uygulama, hem terminal üzerinden (CLI) hem de **FastAPI tabanlı bir REST API** üzerinden kullanılabilir. Ek olarak, kullanıcı dostu bir **HTML arayüzü** ve **Pytest ile yazılmış kapsamlı testler** içermektedir.

-----


## 🚀 Özellikler

  - **Kitap Ekleme, Listeleme ve Silme:** Temel CRUD (Create, Read, Update, Delete) işlemleri ile kütüphane envanterini kolayca yönetin.
  - **Kalıcı Veri Saklama:** Tüm kitap verileri, kolay okunabilir bir JSON dosyası (`library.json`) üzerinde saklanır ve uygulamayı her başlattığınızda verileriniz güvende kalır.
  - **Open Library API Entegrasyonu:** ISBN ile kitap eklerken, başlık ve yazar bilgileri otomatik olarak **Open Library API**'den çekilir, bu da manuel veri girişini minimuma indirir.
  - **Barkod Okuma Desteği:** Kullanıcı arayüzü (UI) üzerinden direkt olarak kamera ile kitapların barkodunu (ISBN) okuyarak hızlı bir şekilde sisteme ekleme imkanı sunar.
  - **Gelişmiş Arama ve Sıralama:** Başlık, yazar veya ISBN'e göre arama yapabilir ve listelenen kitapları başlığa (A-Z) göre sıralayabilirsiniz.
  - **RESTful API:** Tüm kütüphane işlevlerine erişim sağlayan, modern ve standartlara uygun bir FastAPI tabanlı REST API.
  - **Basit ve Kullanışlı HTML Arayüzü:** FastAPI'nin sunduğu basit HTML arayüzü, terminal kullanmak istemeyenler için görsel bir yönetim paneli sağlar.
  - **Pytest ile Kapsamlı Testler:** Projenin sağlamlığını ve güvenilirliğini garanti altına almak için, hem OOP sınıfları hem de API endpointleri için Pytest ile yazılmış testler bulunmaktadır.


-----

## 🔧 Gereksinimler

  - Python 3.9 veya üzeri
  - Gerekli bağımlılıkları yüklemek için `requirements.txt` dosyasını kullanın:

<!-- end list -->

```bash
pip install -r requirements.txt
```

-----

## 📂 Proje Yapısı

```
python_opp_kutuphane/
├── api.py               # FastAPI uygulaması ve endpointleri
├── library.py           # Kütüphane yönetimini sağlayan OOP sınıfları (Book, Library)
├── main.py              # Komut satırı arayüzü (CLI) uygulaması
├── open_library.py      # Open Library API entegrasyonu için modül
├── run_api.py           # API'yi başlatmak için kolaylık sağlayan betik
├── library.json         # Kitap verilerinin JSON formatında saklandığı dosya
├── ui/                  # HTML arayüz dosyalarının bulunduğu klasör
│   └── index.html       # Basit HTML arayüzü
├── tests/               # Pytest test dosyaları
│   ├── __init__.py
│   ├── test_api_endpoints.py # API endpointlerini test eder
│   ├── test_library.py       # OOP yapısını test eder
│   └── test_main.py          # CLI işlevlerini test eder
├── requirements.txt     # Proje bağımlılıkları
└── API_KULLANIM_KILAVUZU.md # API kullanımı hakkında detaylı bilgi
```

-----

## ▶️ Uygulamayı Çalıştırma

### CLI (Komut Satırı Arayüzü)

Terminal üzerinden uygulamayı başlatmak için:

```bash
python main.py
```

Bu modda, veriler aynı klasördeki `library.json` dosyasında kalıcı olarak saklanır.

### API ve HTML Arayüzü

RESTful API ve HTML arayüzünü çalıştırmak için `uvicorn` kullanın:

```bash
uvicorn api:app --reload
```

  - **Ana Sayfa (HTML UI):** `http://127.0.0.1:8000/`
  - **Swagger UI:** `http://127.0.0.1:8000/docs` (API endpointlerini test etmek için interaktif arayüz)
  - **Health Check:** `http://127.0.0.1:8000/health` (Uygulamanın çalışır durumda olup olmadığını kontrol eder)

### 🌐 Kullanıcı Arayüzü Detayları

HTML arayüzü, `ui/index.html` dosyası üzerinden sunulur ve aşağıdaki işlevleri içerir:

  - **Kitap Ekleme Formu:** ISBN girerek veya barkod okuyucu ile yeni kitap ekleyebilirsiniz.
  - **Barkod Okuyucu:** "Barkod Tara" butonu, kullanıcının kamerasını açar ve kitabın ISBN'ini barkoddan okuyarak otomatik olarak formu doldurur.
  - **Kitap Listesi:** Eklenmiş tüm kitapları tabloda listeler. Tablo, **ISBN, Başlık** ve **Yazar** sütunlarını içerir.
  - **Arama ve Sıralama:** "Başlık, yazar, ISBN" alanına anahtar kelime yazarak arama yapabilir ve "Başlık (Z-A)" veya "Başlık (A-Z)" seçenekleriyle sıralayabilirsiniz.
  - **Silme İşlemleri:**
      - Her satırın yanında bulunan "Sil" butonu ile tek bir kitabı silebilirsiniz.
      - Tablodan birden fazla kitap seçerek "Seçiliyi Sil" butonu ile toplu silme işlemi gerçekleştirebilirsiniz.
      - "Hepsini seç" onay kutusu ile listedeki tüm kitapları seçebilirsiniz.


-----
<img width="2875" height="1403" alt="ui_library" src="https://github.com/user-attachments/assets/d4b83a57-1a93-41be-8580-9384bc7d4f75" />
<img width="2878" height="1405" alt="barcode reader" src="https://github.com/user-attachments/assets/df9fa7e8-1774-4430-89b8-0eb3c8cccce6" />

## 🧪 Testler

Projenin güvenilirliğini sağlamak amacıyla Pytest ile yazılmış testler, farklı katmanlardaki işlevleri kapsar:

```bash
python -m pytest -q tests
```

  - `test_library.py`: `Book` ve `Library` sınıflarının doğru çalıştığını, kitap ekleme, silme ve listeleme gibi temel OOP mantığını test eder.
  - `test_api_endpoints.py`: API'nin tüm endpointlerinin (GET, POST, DELETE) doğru HTTP yanıtları verdiğini ve istenen işlemleri başarıyla gerçekleştirdiğini doğrular.
  - `test_main.py`: CLI (Komut Satırı Arayüzü) modülünün beklendiği gibi çalıştığını test eder.

-----

## 📖 Özet

Bu proje, Python OOP mantığıyla tasarlanmış bir kütüphane yönetim sistemini hem CLI hem de REST API üzerinden kullanılabilir hale getirir. JSON tabanlı kalıcı veri saklama, Open Library entegrasyonu ve barkod okuma gibi modern özelliklerle zenginleştirilmiştir. Özellikle yazılım geliştirme öğrenenler için nesne yönelimli programlama, RESTful API geliştirme, frontend ile backend iletişimi ve test yazma konularında pratik bir örnek niteliği taşır.
