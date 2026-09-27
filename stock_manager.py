"""
stock_manager.py
------------------
StockFlow CLI - Stok Durumu.

Satış yapıldığında stok zaten sales_manager.py içinde otomatik düşüyor
(stok = stok - satılan_adet). Bu modül ise stoğa ekleme
(stok = stok + eklenen_adet) ve düşük stok raporunu yönetir.
"""

from inventory_manager import ProductManager
from exceptions import ProductNotFoundError, InvalidQuantityError
from utils import input_int


class StockManager:
    """Stok ekleme ve düşük stok tespiti işlemlerini yönetir."""

    def __init__(self, product_manager: ProductManager):
        self.product_manager = product_manager

    def restock(self, product_id, quantity):
        """stok = stok + eklenen_adet"""
        product = self.product_manager.get_product(product_id)  # yoksa ProductNotFoundError

        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidQuantityError("Eklenecek miktar sıfırdan büyük bir tam sayı olmalı.")

        product.stock = product.stock + quantity
        return product

    def get_low_stock_products(self):
        """minimum_stok değerine göre stoğu azalan/eşit olan ürünleri döndürür."""
        return [p for p in self.product_manager.list_products() if p.is_low_stock]


# ==========================================================
#                    ARA YÜZ (CLI) FONKSİYONLARI
# ==========================================================

def restock_interactive(manager: StockManager):
    print("\n--- Stok Ekle ---")
    try:
        product_id = input_int("Ürün ID: ")
        quantity = input_int("Eklenecek adet: ")
        product = manager.restock(product_id, quantity)
        print(f"\n✓ Stok güncellendi.\nYeni stok: {product.stock}")
    except ProductNotFoundError as e:
        print(f"\n❌ {e}")
    except InvalidQuantityError as e:
        print(f"\n❌ {e}")


def low_stock_report_interactive(manager: StockManager):
    print("\n⚠️ DÜŞÜK STOK\n")
    low_stock_products = manager.get_low_stock_products()
    if not low_stock_products:
        print("Düşük stoklu ürün yok.")
        return
    for product in low_stock_products:
        print(f"{product.name:<20} {product.stock} adet")


def full_stock_status_interactive(manager: StockManager):
    print("\n--- Tüm Stok Durumu ---")
    products = manager.product_manager.list_products()
    if not products:
        print("Kayıtlı ürün yok.")
        return
    for product in products:
        uyari = "  ⚠️ Düşük stok!" if product.is_low_stock else ""
        print(f"{product.name:<20} {product.stock} adet{uyari}")


def run_stock_menu(manager: StockManager):
    """Stok Durumu menüsünü çalıştırır."""
    while True:
        print(
            "\nStok Durumu\n\n"
            "1. Stok ekle\n"
            "2. Düşük stok raporu\n"
            "3. Tüm stok durumu\n"
            "0. Geri"
        )
        choice = input("Seçiminiz: ").strip()

        if choice == "0":
            break
        elif choice == "1":
            restock_interactive(manager)
        elif choice == "2":
            low_stock_report_interactive(manager)
        elif choice == "3":
            full_stock_status_interactive(manager)
        else:
            print("❌ Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    # Hızlı manuel test
    pm = ProductManager()
    pm.add_product("Logitech G102", "Elektronik", 799.99, 3, 5)   # düşük stok (3 <= 5)
    pm.add_product("Samsung SSD", "Elektronik", 1299.00, 2, 10)   # düşük stok
    pm.add_product("HDMI Kablo", "Aksesuar", 89.90, 4, 15)        # düşük stok
    pm.add_product("Monitör", "Elektronik", 4999.00, 25, 5)       # normal

    sm = StockManager(pm)
    run_stock_menu(sm)
