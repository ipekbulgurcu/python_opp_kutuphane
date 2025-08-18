"""
Python ile API Etkileşimi: Tüm HTTP Metotları
Bu dosya, API notebook'undaki tüm kod örneklerini içerir.
"""

import httpx
import json


def main():
    """Main function demonstrating all HTTP methods."""
    print("=== Python ile API Etkileşimi: HTTP Metotları Demo ===\n")

    # Setup
    print("Kurulum tamamlandı!")

    # Demonstrate all HTTP methods
    demo_get_request()
    demo_post_request()
    demo_put_request()
    demo_patch_request()
    demo_delete_request()

    print("\n=== Demo Tamamlandı ===")


def demo_get_request():
    """Demonstrate GET request - Reading data from server."""
    print("\n--- GET İsteği: Open Library'den Kitap Arama ---")
    OPEN_LIBRARY_URL = "https://openlibrary.org/search.json"
    params = {"title": "Dune", "author": "Frank Herbert", "limit": 3}

    try:
        response = httpx.get(OPEN_LIBRARY_URL, params=params)
        # raise_for_status(), 4xx veya 5xx durum kodlarında bir hata fırlatır
        response.raise_for_status()

        data = response.json()
        print(f"'{params['title']}' için {data.get('numFound', 0)} sonuç bulundu.")
        if data.get('docs'):
            first_book = data['docs'][0]
            print(f"İlk Sonuç: {first_book.get('title')} ({first_book.get('first_publish_year')})")
    except httpx.HTTPStatusError as e:
        print(f"Hata! API yanıtı: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"İstek hatası: {e}")


def demo_post_request():
    """Demonstrate POST request - Creating new data on server."""
    print("\n--- POST İsteği: Yeni Bir Blog Yazısı Oluşturma ---")
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"

    # Göndereceğimiz yeni yazı verisi
    new_post = {
        'title': 'Python ve APIlar',
        'body': 'httpx kütüphanesi ile APIlerle çalışmak çok kolay.',
        'userId': 10
    }

    try:
        response = httpx.post(f"{JSONPLACEHOLDER_URL}/posts", json=new_post)
        response.raise_for_status()

        print(f"Durum Kodu: {response.status_code}")  # Başarılı bir POST genellikle '201 Created' döndürür
        print("Oluşturulan Kaynak:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except httpx.HTTPStatusError as e:
        print(f"POST Hatası: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"İstek hatası: {e}")


def demo_put_request():
    """Demonstrate PUT request - Completely updating existing data."""
    print("\n--- PUT İsteği: Bir Yazıyı Tamamen Güncelleme ---")
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
    post_id_to_update = 1

    # Kaynağın tüm alanlarını içeren yeni veri
    updated_post_data = {
        'id': post_id_to_update,
        'title': 'Tamamen Güncellenmiş Başlık',
        'body': 'Bu içerik PUT metodu ile tamamen değiştirildi.',
        'userId': 1
    }

    try:
        response = httpx.put(f"{JSONPLACEHOLDER_URL}/posts/{post_id_to_update}", json=updated_post_data)
        response.raise_for_status()

        print(f"Durum Kodu: {response.status_code}")
        print("Güncellenmiş Kaynak:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except httpx.HTTPStatusError as e:
        print(f"PUT Hatası: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"İstek hatası: {e}")


def demo_patch_request():
    """Demonstrate PATCH request - Partially updating existing data."""
    print("\n--- PATCH İsteği: Bir Yazının Sadece Başlığını Güncelleme ---")
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
    post_id_to_patch = 1

    # Sadece değiştirmek istediğimiz alanı gönderiyoruz
    patch_data = {'title': 'Kısmen Güncellenmiş Başlık (PATCH)'}

    try:
        response = httpx.patch(f"{JSONPLACEHOLDER_URL}/posts/{post_id_to_patch}", json=patch_data)
        response.raise_for_status()

        print(f"Durum Kodu: {response.status_code}")
        print("Kısmen Güncellenmiş Kaynak:")
        print(json.dumps(response.json(), indent=2, ensure_ascii=False))
    except httpx.HTTPStatusError as e:
        print(f"PATCH Hatası: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"İstek hatası: {e}")


def demo_delete_request():
    """Demonstrate DELETE request - Removing data from server."""
    print("\n--- DELETE İsteği: Bir Yazıyı Silme ---")
    JSONPLACEHOLDER_URL = "https://jsonplaceholder.typicode.com"
    post_id_to_delete = 1

    try:
        response = httpx.delete(f"{JSONPLACEHOLDER_URL}/posts/{post_id_to_delete}")
        response.raise_for_status()

        print(f"Durum Kodu: {response.status_code}")  # Başarılı silme genellikle '200 OK' döndürür
        print("Dönen Yanıt (genellikle boştur):")
        print(response.json())  # Başarılı bir DELETE sonrası yanıt gövdesi genellikle boştur
    except httpx.HTTPStatusError as e:
        print(f"DELETE Hatası: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"İstek hatası: {e}")


def test_all_methods():
    """Test function to verify all HTTP methods work correctly."""
    print("\n=== Testing All HTTP Methods ===")

    try:
        # Test GET
        response = httpx.get("https://jsonplaceholder.typicode.com/posts/1")
        assert response.status_code == 200
        print("✅ GET test passed")

        # Test POST
        response = httpx.post("https://jsonplaceholder.typicode.com/posts",
                             json={"title": "test", "body": "test", "userId": 1})
        assert response.status_code == 201
        print("✅ POST test passed")

        # Test PUT
        response = httpx.put("https://jsonplaceholder.typicode.com/posts/1",
                            json={"id": 1, "title": "test", "body": "test", "userId": 1})
        assert response.status_code == 200
        print("✅ PUT test passed")

        # Test PATCH
        response = httpx.patch("https://jsonplaceholder.typicode.com/posts/1",
                              json={"title": "updated"})
        assert response.status_code == 200
        print("✅ PATCH test passed")

        # Test DELETE
        response = httpx.delete("https://jsonplaceholder.typicode.com/posts/1")
        assert response.status_code == 200
        print("✅ DELETE test passed")

        print("🎉 All HTTP methods work correctly!")

    except Exception as e:
        print(f"❌ Test failed: {e}")


def demonstrate_error_handling():
    """Demonstrate proper error handling with HTTP requests."""
    print("\n=== Error Handling Demo ===")

    # Test with invalid URL
    try:
        response = httpx.get("https://invalid-url-that-does-not-exist.com")
        response.raise_for_status()
    except httpx.RequestError as e:
        print(f"✅ Caught network error as expected: {type(e).__name__}")

    # Test with 404 error
    try:
        response = httpx.get("https://jsonplaceholder.typicode.com/posts/99999")
        response.raise_for_status()
    except httpx.HTTPStatusError as e:
        print(f"✅ Caught HTTP error as expected: {e.response.status_code}")

    print("Error handling works correctly!")


def demonstrate_advanced_features():
    """Demonstrate advanced httpx features."""
    print("\n=== Advanced HTTP Features ===")

    # Custom headers
    headers = {
        "User-Agent": "Python HTTP Demo/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }

    # Timeout configuration
    timeout = httpx.Timeout(10.0)

    # Using context manager for automatic resource cleanup
    with httpx.Client(headers=headers, timeout=timeout) as client:
        response = client.get("https://jsonplaceholder.typicode.com/posts/1")
        print(f"Response with custom headers: {response.status_code}")
        print(f"Content-Type: {response.headers.get('content-type')}")

    print("✅ Advanced features demonstrated")


def show_http_methods_summary():
    """Display summary table of HTTP methods."""
    print("\n=== HTTP Metotları Özeti ===")
    print("| Metot  | Amaç                              | Güvenli* | Idempotent** |")
    print("|--------|-----------------------------------|----------|--------------|")
    print("| GET    | Veri okur                         | Evet     | Evet         |")
    print("| POST   | Yeni veri oluşturur               | Hayır    | Hayır        |")
    print("| PUT    | Veriyi tamamen değiştirir         | Hayır    | Evet         |")
    print("| PATCH  | Veriyi kısmen günceller           | Hayır    | Hayır        |")
    print("| DELETE | Veriyi siler                      | Hayır    | Evet         |")
    print("\n*Güvenli: Metot, sunucudaki durumu değiştirmez.")
    print("**Idempotent: Aynı isteği birden çok kez tekrarlamak, ilk istekten farklı bir sonuca yol açmaz.")


if __name__ == "__main__":
    # Run the main demo
    main()

    # Run tests
    test_all_methods()

    # Demonstrate error handling
    demonstrate_error_handling()

    # Show advanced features
    demonstrate_advanced_features()

    # Show summary
    show_http_methods_summary()