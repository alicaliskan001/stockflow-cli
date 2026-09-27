"""
reports_manager.py
---------------------
StockFlow CLI - Raporlar.

ProductManager ve SaleManager'daki verileri birleştirip işletme sahibine
anlamlı özetler sunar: toplam ürün/stok, toplam satış/ciro, en çok satan
ürün, düşük stoklu ürünler, kategori bazlı satışlar.
"""

from collections import defaultdict

from inventory_manager import ProductManager
from sales_manager import SaleManager


def format_try(amount):
    """1234.5 -> '₺1.234,50' (Türkçe para birimi formatı)."""
    s = f"{amount:,.2f}"                 # '1,234.50'
    s = s.replace(",", "X").replace(".", ",").replace("X", ".")  # '1.234,50'
    return f"₺{s}"


class ReportManager:
    """Ürün ve satış verilerinden rapor üreten sınıf."""

    def __init__(self, product_manager: ProductManager, sale_manager: SaleManager):
        self.product_manager = product_manager
        self.sale_manager = sale_manager

    # ---------- 1. Toplam ürün sayısı ----------
    def total_product_count(self):
        return len(self.product_manager.list_products())

    # ---------- 2. Toplam stok miktarı ----------
    def total_stock_quantity(self):
        return sum(p.stock for p in self.product_manager.list_products())

    # ---------- 3. Toplam satış (işlem sayısı) ----------
    def total_sales_count(self):
        return len(self.sale_manager.list_sales())

    # ---------- 4. Toplam ciro ----------
    def total_revenue(self):
        return sum(sale.total_amount for sale in self.sale_manager.list_sales())

    # ---------- 5. En çok satılan ürün (satılan adete göre) ----------
    def best_selling_product(self):
        qty_by_product = defaultdict(int)
        name_by_id = {}
        for sale in self.sale_manager.list_sales():
            qty_by_product[sale.product.product_id] += sale.quantity
            name_by_id[sale.product.product_id] = sale.product.name

        if not qty_by_product:
            return None, 0

        best_id = max(qty_by_product, key=qty_by_product.get)
        return name_by_id[best_id], qty_by_product[best_id]

    # ---------- 6. Düşük stoklu ürünler ----------
    def low_stock_products(self):
        return [p for p in self.product_manager.list_products() if p.is_low_stock]

    # ---------- 7. Kategori bazlı satışlar ----------
    def sales_by_category(self):
        qty_by_category = defaultdict(int)
        revenue_by_category = defaultdict(float)
        for sale in self.sale_manager.list_sales():
            category = sale.product.category
            qty_by_category[category] += sale.quantity
            revenue_by_category[category] += sale.total_amount
        return qty_by_category, revenue_by_category


# ==========================================================
#                    ARA YÜZ (CLI) FONKSİYONLARI
# ==========================================================

def report_total_products(manager: ReportManager):
    print(f"\nToplam ürün sayısı: {manager.total_product_count()}")


def report_total_stock(manager: ReportManager):
    print(f"\nToplam stok miktarı: {manager.total_stock_quantity()} adet")


def report_total_sales(manager: ReportManager):
    print(f"\nToplam satış: {manager.total_sales_count()}")


def report_total_revenue(manager: ReportManager):
    print(f"\nToplam ciro:\n{format_try(manager.total_revenue())}")


def report_best_seller(manager: ReportManager):
    name, qty = manager.best_selling_product()
    if name is None:
        print("\nHenüz satış yok.")
        return
    print(f"\nEn çok satan ürün:\n{name}\n\nSatış adedi:\n{qty}")


def report_low_stock(manager: ReportManager):
    products = manager.low_stock_products()
    print(f"\nDüşük stoklu ürün: {len(products)}")
    if products:
        print()
        for p in products:
            print(f"{p.name:<20} {p.stock} adet")


def report_sales_by_category(manager: ReportManager):
    qty_by_category, revenue_by_category = manager.sales_by_category()
    if not qty_by_category:
        print("\nHenüz satış yok.")
        return
    print()
    for category in qty_by_category:
        print(
            f"{category:<15} {qty_by_category[category]} adet   "
            f"{format_try(revenue_by_category[category])}"
        )


def report_general_summary(manager: ReportManager):
    """Örnekteki 'SATIŞ RAPORU' özetini üretir."""
    name, qty = manager.best_selling_product()
    print("\n════════ SATIŞ RAPORU ════════\n")
    print(f"Toplam satış: {manager.total_sales_count()}\n")
    print(f"Toplam ciro:\n{format_try(manager.total_revenue())}\n")
    if name is not None:
        print(f"En çok satan ürün:\n{name}\n")
        print(f"Satış adedi:\n{qty}\n")
    else:
        print("En çok satan ürün:\nHenüz satış yok.\n")
    print(f"Düşük stoklu ürün:\n{len(manager.low_stock_products())}")


def run_reports_menu(manager: ReportManager):
    """Raporlar menüsünü çalıştırır."""
    actions = {
        "1": report_total_products,
        "2": report_total_stock,
        "3": report_total_sales,
        "4": report_total_revenue,
        "5": report_best_seller,
        "6": report_low_stock,
        "7": report_sales_by_category,
        "8": report_general_summary,
    }

    while True:
        print(
            "\n════════════ RAPORLAR ════════════\n\n"
            "1. Toplam ürün sayısı\n"
            "2. Toplam stok miktarı\n"
            "3. Toplam satış\n"
            "4. Toplam ciro\n"
            "5. En çok satılan ürün\n"
            "6. Düşük stoklu ürünler\n"
            "7. Kategori bazlı satışlar\n"
            "8. Genel özet\n"
            "0. Geri"
        )
        choice = input("Seçiminiz: ").strip()

        if choice == "0":
            break
        action = actions.get(choice)
        if action:
            action(manager)
        else:
            print("❌ Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    # Hızlı manuel test
    pm = ProductManager()
    p1 = pm.add_product("Logitech G102", "Elektronik", 799.99, 30, 5)
    p2 = pm.add_product("Samsung SSD", "Elektronik", 1299.00, 10, 10)
    p3 = pm.add_product("HDMI Kablo", "Aksesuar", 89.90, 25, 15)

    sm = SaleManager(pm)
    sm.create_sale(p1.product_id, 23)
    sm.create_sale(p2.product_id, 5)
    sm.create_sale(p3.product_id, 19)

    rm = ReportManager(pm, sm)
    run_reports_menu(rm)
