"""
persistence_manager.py
------------------------
StockFlow CLI - JSON ile Kalıcı Veri Saklama.

Program kapatılınca veriler kaybolmasın diye ürünleri data/products.json'a,
satışları data/sales.json'a kaydeder; program açılırken de bu dosyalardan
geri okuyup Product / Sale nesnelerine çevirir.

Dönüşüm akışı:
    Kaydederken:  Product / Sale nesneleri -> dict/list -> JSON dosyası
    Yüklerken:    JSON dosyası -> dict/list -> Product / Sale nesneleri
"""

import json
import os
from datetime import datetime

from product import product_from_dict
from sale import Sale
from inventory_manager import ProductManager
from sales_manager import SaleManager
from exceptions import DataPersistenceError, ProductNotFoundError


class DataManager:
    """Ürün ve satış verilerini JSON dosyalarıyla senkronize eden sınıf."""

    def __init__(self, product_manager: ProductManager, sale_manager: SaleManager,
                 data_dir="data"):
        self.product_manager = product_manager
        self.sale_manager = sale_manager
        self.data_dir = data_dir
        self.products_file = os.path.join(data_dir, "products.json")
        self.sales_file = os.path.join(data_dir, "sales.json")

    # ==========================================================
    #                        KAYDETME (SAVE)
    #        Product / Sale nesneleri -> dict/list -> JSON
    # ==========================================================
    def save_products(self):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            data = [p.to_dict() for p in self.product_manager.list_products()]
            with open(self.products_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise DataPersistenceError(f"Ürünler kaydedilemedi: {e}")

    def save_sales(self):
        try:
            os.makedirs(self.data_dir, exist_ok=True)
            data = [s.to_dict() for s in self.sale_manager.list_sales()]
            with open(self.sales_file, "w", encoding="utf-8") as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
        except OSError as e:
            raise DataPersistenceError(f"Satışlar kaydedilemedi: {e}")

    def save_all(self):
        self.save_products()
        self.save_sales()

    # ==========================================================
    #                        YÜKLEME (LOAD)
    #        JSON -> dict/list -> Product / Sale nesneleri
    # ==========================================================
    def load_products(self):
        if not os.path.exists(self.products_file):
            return
        try:
            with open(self.products_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise DataPersistenceError(f"Ürünler yüklenemedi: {e}")

        self.product_manager.products.clear()
        max_id = 0
        for item in data:
            product = product_from_dict(item)   # dict -> Product/PhysicalProduct/DigitalProduct
            self.product_manager.products[product.product_id] = product
            max_id = max(max_id, product.product_id)
        if data:
            self.product_manager._next_id = max_id + 1

    def load_sales(self):
        if not os.path.exists(self.sales_file):
            return
        try:
            with open(self.sales_file, "r", encoding="utf-8") as f:
                data = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise DataPersistenceError(f"Satışlar yüklenemedi: {e}")

        self.sale_manager.sales.clear()
        max_id = 0
        for item in data:
            try:
                product = self.product_manager.get_product(item["product_id"])
            except ProductNotFoundError:
                continue  # ürünü silinmiş bir satış varsa atla

            date = datetime.strptime(item["date"], "%Y-%m-%d %H:%M:%S")
            sale = Sale(item["sale_id"], product, item["quantity"], date=date)
            self.sale_manager.sales[sale.sale_id] = sale
            max_id = max(max_id, sale.sale_id)
        if data:
            self.sale_manager._next_id = max_id + 1

    def load_all(self):
        self.load_products()
        self.load_sales()  # satışlar, ürünlere referans verdiği için ürünlerden SONRA yüklenmeli


# ==========================================================
#                    ARA YÜZ (CLI) FONKSİYONLARI
# ==========================================================

def backup_interactive(manager: DataManager):
    print("\n--- Verileri Yedekle ---")
    try:
        manager.save_all()
        print(
            f"\n✓ Veriler kaydedildi.\n"
            f"  {manager.products_file}\n"
            f"  {manager.sales_file}"
        )
    except DataPersistenceError as e:
        print(f"\n❌ {e}")


def restore_interactive(manager: DataManager):
    print("\n--- Verileri Yükle ---")
    try:
        manager.load_all()
        print(
            f"\n✓ Veriler yüklendi.\n"
            f"  Ürün sayısı: {len(manager.product_manager.list_products())}\n"
            f"  Satış sayısı: {len(manager.sale_manager.list_sales())}"
        )
    except DataPersistenceError as e:
        print(f"\n❌ {e}")


if __name__ == "__main__":
    # Hızlı manuel test: kaydet -> sıfırla -> yükle -> karşılaştır
    pm = ProductManager()
    p1 = pm.add_product("Logitech G102", "Elektronik", 799.99, 17, 5)
    sm = SaleManager(pm)
    sm.create_sale(p1.product_id, 3)

    dm = DataManager(pm, sm, data_dir="data")
    dm.save_all()
    print("Kaydedildi ->", dm.products_file, "/", dm.sales_file)

    # Sıfırdan yeni yöneticilerle yükleyelim
    pm2 = ProductManager()
    sm2 = SaleManager(pm2)
    dm2 = DataManager(pm2, sm2, data_dir="data")
    dm2.load_all()

    print("\nYüklenen ürünler:")
    for p in pm2.list_products():
        print(p)
        print()

    print("Yüklenen satışlar:")
    for s in sm2.list_sales():
        print(s)
        print()
