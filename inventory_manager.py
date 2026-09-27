"""
inventory_manager.py
---------------------
StockFlow CLI - Ürün Yönetimi.

Bu modül, product.py'deki Product sınıfını kullanarak ürünlerin
eklenmesi, silinmesi, güncellenmesi, listelenmesi ve aranmasını
yöneten ProductManager sınıfını içerir. Ayrıca "Ürün Yönetimi"
alt menüsünü çalıştıran run_product_menu() fonksiyonu burada yer alır.

Kullanılan konular: OOP (Product ile birlikte), exception handling,
dict/list veri yapıları.
"""

from product import Product
from exceptions import ProductNotFoundError, InvalidProductDataError
from utils import input_float, input_int


class ProductManager:
    """Ürünlerin tutulduğu ve yönetildiği sınıf."""

    def __init__(self, start_id=1001):
        self.products = {}          # {product_id: Product}
        self._next_id = start_id

    # ---------- ID üretimi ----------
    def _generate_id(self):
        new_id = self._next_id
        self._next_id += 1
        return new_id

    # ---------- CRUD işlemleri ----------
    def add_product(self, name, category, price, stock, min_stock):
        if not name or not name.strip():
            raise InvalidProductDataError("Ürün adı boş olamaz.")
        if not category or not category.strip():
            raise InvalidProductDataError("Kategori boş olamaz.")

        product_id = self._generate_id()
        product = Product(product_id, name.strip(), category.strip(), price, stock, min_stock)
        self.products[product_id] = product
        return product

    def get_product(self, product_id):
        try:
            return self.products[product_id]
        except KeyError:
            raise ProductNotFoundError(f"{product_id} ID'li ürün bulunamadı.")

    def delete_product(self, product_id):
        product = self.get_product(product_id)  # yoksa zaten exception fırlatır
        del self.products[product_id]
        return product

    def update_product(self, product_id, name=None, category=None,
                        price=None, stock=None, min_stock=None):
        product = self.get_product(product_id)

        if name is not None and name.strip():
            product.name = name.strip()
        if category is not None and category.strip():
            product.category = category.strip()
        if price is not None:
            product.price = price          # setter doğrulama yapar
        if stock is not None:
            product.stock = stock          # setter doğrulama yapar
        if min_stock is not None:
            product.min_stock = min_stock  # setter doğrulama yapar

        return product

    def list_products(self):
        return list(self.products.values())

    def search_product(self, keyword):
        keyword = keyword.lower().strip()
        return [
            p for p in self.products.values()
            if keyword in p.name.lower() or keyword in p.category.lower()
        ]


# ==========================================================
#                    ARA YÜZ (CLI) FONKSİYONLARI
# ==========================================================

def add_product_interactive(manager: ProductManager):
    print("\n--- Ürün Ekle ---")
    name = input("Ürün adı: ").strip()
    category = input("Kategori: ").strip()
    price = input_float("Fiyat: ")
    stock = input_int("Stok: ")
    min_stock = input_int("Minimum stok: ")

    try:
        product = manager.add_product(name, category, price, stock, min_stock)
        print(f"\n✓ Ürün başarıyla eklendi.\nÜrün ID: {product.product_id}")
    except InvalidProductDataError as e:
        print(f"\n✗ Hata: {e}")
    except (TypeError, ValueError) as e:
        print(f"\n✗ Geçersiz veri: {e}")


def delete_product_interactive(manager: ProductManager):
    print("\n--- Ürün Sil ---")
    try:
        product_id = input_int("Silinecek ürün ID: ")
        product = manager.delete_product(product_id)
        print(f"\n✓ '{product.name}' ürünü silindi.")
    except ProductNotFoundError as e:
        print(f"\n✗ Hata: {e}")


def update_product_interactive(manager: ProductManager):
    print("\n--- Ürün Güncelle ---")
    try:
        product_id = input_int("Güncellenecek ürün ID: ")
        manager.get_product(product_id)  # önce var mı diye kontrol et

        print("(Değiştirmek istemediğiniz alanı boş bırakıp Enter'a basın)")
        name = input("Yeni ürün adı: ").strip() or None
        category = input("Yeni kategori: ").strip() or None

        price_raw = input("Yeni fiyat: ").strip()
        price = float(price_raw.replace(",", ".")) if price_raw else None

        stock_raw = input("Yeni stok: ").strip()
        stock = int(stock_raw) if stock_raw else None

        min_stock_raw = input("Yeni minimum stok: ").strip()
        min_stock = int(min_stock_raw) if min_stock_raw else None

        product = manager.update_product(
            product_id, name=name, category=category,
            price=price, stock=stock, min_stock=min_stock
        )
        print(f"\n✓ Ürün güncellendi:\n{product}")
    except ProductNotFoundError as e:
        print(f"\n✗ Hata: {e}")
    except (TypeError, ValueError) as e:
        print(f"\n✗ Geçersiz veri: {e}")


def list_products_interactive(manager: ProductManager):
    print("\n--- Ürün Listesi ---")
    products = manager.list_products()
    if not products:
        print("Kayıtlı ürün yok.")
        return
    for product in products:
        print()
        print(product)
        if product.is_low_stock:
            print("⚠ Stok azalıyor!")


def search_product_interactive(manager: ProductManager):
    print("\n--- Ürün Ara ---")
    keyword = input("Aranacak ürün adı / kategori: ").strip()
    results = manager.search_product(keyword)
    if not results:
        print("Sonuç bulunamadı.")
        return
    for product in results:
        print()
        print(product)


def run_product_menu(manager: ProductManager):
    """Ürün Yönetimi alt menüsünü çalıştırır."""
    actions = {
        "1": add_product_interactive,
        "2": delete_product_interactive,
        "3": update_product_interactive,
        "4": list_products_interactive,
        "5": search_product_interactive,
    }

    while True:
        print(
            "\n1. Ürün ekle\n"
            "2. Ürün sil\n"
            "3. Ürün güncelle\n"
            "4. Ürünleri listele\n"
            "5. Ürün ara\n"
            "0. Geri"
        )
        choice = input("Seçiminiz: ").strip()

        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("✗ Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    # Hızlı manuel test
    manager = ProductManager()
    run_product_menu(manager)
