"""
test_manual.py
----------------
StockFlow CLI - Manuel Test Senaryoları.

Tam bir test framework'ü (pytest/unittest) yerine, projenin kritik
davranışlarını (stok düşürme, yetersiz stok, geçersiz fiyat, olmayan
ürün) doğrulayan basit, okunabilir senaryolar. assert + try/except
kullanır; her test PASS/FAIL olarak raporlanır.

Çalıştırmak için:  python3 test_manual.py
"""

from inventory_manager import ProductManager
from sales_manager import SaleManager
from exceptions import InsufficientStockError, ProductNotFoundError


def test_1_urun_olustur():
    print("\nTest 1: 100 TL fiyatlı, 5 stoklu ürün oluştur")
    pm = ProductManager()
    p = pm.add_product("Test Ürünü", "Test", 100, 5, 1)

    assert p.price == 100, f"Beklenen fiyat 100, gelen {p.price}"
    assert p.stock == 5, f"Beklenen stok 5, gelen {p.stock}"

    print(f"✓ PASS - Ürün oluşturuldu: {p.name} | Fiyat: {p.price} TL | Stok: {p.stock}")
    return pm, p


def test_2_satis(pm, product):
    print("\nTest 2: 3 adet sat")
    sm = SaleManager(pm)
    sm.create_sale(product.product_id, 3)

    assert product.stock == 2, f"Beklenen stok 2, gelen {product.stock}"

    print(f"✓ PASS - Satış sonrası stok: {product.stock}")
    return sm


def test_3_yetersiz_stok(sm, product):
    print("\nTest 3: 10 adet satmaya çalış (mevcut stok: 2)")
    try:
        sm.create_sale(product.product_id, 10)
        print("✗ FAIL - Hata bekleniyordu ama satış gerçekleşti.")
    except InsufficientStockError:
        print("✓ PASS - ❌ Yetersiz stok.")


def test_4_gecersiz_fiyat():
    print("\nTest 4: -100 TL fiyatla ürün oluşturmaya çalış")
    pm = ProductManager()
    try:
        pm.add_product("Hatalı Ürün", "Test", -100, 5, 1)
        print("✗ FAIL - Hata bekleniyordu ama ürün oluşturuldu.")
    except (ValueError, TypeError):
        print("✓ PASS - ❌ Geçersiz fiyat.")


def test_5_olmayan_urun():
    print("\nTest 5: Olmayan ürün, ID: 9999")
    pm = ProductManager()
    try:
        pm.get_product(9999)
        print("✗ FAIL - Hata bekleniyordu ama ürün bulundu.")
    except ProductNotFoundError:
        print("✓ PASS - ❌ Ürün bulunamadı.")


def run_all_tests():
    print("=" * 50)
    print("STOCKFLOW CLI - MANUEL TEST SENARYOLARI")
    print("=" * 50)

    pm, product = test_1_urun_olustur()
    sm = test_2_satis(pm, product)
    test_3_yetersiz_stok(sm, product)
    test_4_gecersiz_fiyat()
    test_5_olmayan_urun()

    print("\n" + "=" * 50)
    print("Tüm testler tamamlandı.")
    print("=" * 50)


if __name__ == "__main__":
    run_all_tests()
