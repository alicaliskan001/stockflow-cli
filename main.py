"""
main.py
--------
StockFlow CLI - Ana Program.

Tüm modülleri (ürün, satış, stok, rapor, JSON kalıcılık) birbirine
bağlayan giriş noktası. Program açılırken JSON'dan veri yükler,
kapanırken JSON'a kaydeder; böylece bilgiler kaybolmaz.
"""

from inventory_manager import ProductManager, run_product_menu, search_product_interactive
from sales_manager import SaleManager, run_sales_menu
from stock_manager import StockManager, run_stock_menu
from reports_manager import ReportManager, run_reports_menu
from persistence_manager import DataManager, backup_interactive, restore_interactive
from exceptions import DataPersistenceError


MAIN_MENU = """
╔══════════════════════════════════════════╗
║             STOCKFLOW CLI                 ║
║       Stok ve Satış Yönetim Sistemi       ║
╠══════════════════════════════════════════╣
║  1. Ürün Yönetimi                         ║
║  2. Satış Yönetimi                        ║
║  3. Stok Durumu                           ║
║  4. Raporlar                              ║
║  5. Ürün Ara                              ║
║  6. Verileri Yedekle                      ║
║  7. Verileri Yükle                        ║
║  0. Çıkış                                 ║
╚══════════════════════════════════════════╝
"""


def main():
    # ---------- Yöneticileri kur ----------
    product_manager = ProductManager()
    sale_manager = SaleManager(product_manager)
    stock_manager = StockManager(product_manager)
    report_manager = ReportManager(product_manager, sale_manager)
    data_manager = DataManager(product_manager, sale_manager)

    # ---------- Program açılırken JSON'dan yükle ----------
    try:
        data_manager.load_all()
    except DataPersistenceError as e:
        print(f"❌ {e}")

    # ---------- Ana döngü ----------
    while True:
        print(MAIN_MENU)
        choice = input("Seçiminiz: ").strip()

        if choice == "1":
            run_product_menu(product_manager)
        elif choice == "2":
            run_sales_menu(sale_manager)
        elif choice == "3":
            run_stock_menu(stock_manager)
        elif choice == "4":
            run_reports_menu(report_manager)
        elif choice == "5":
            search_product_interactive(product_manager)
        elif choice == "6":
            backup_interactive(data_manager)
        elif choice == "7":
            restore_interactive(data_manager)
        elif choice == "0":
            # ---------- Program kapanırken JSON'a kaydet ----------
            try:
                data_manager.save_all()
                print("\n✓ Veriler kaydedildi. Görüşmek üzere!")
            except DataPersistenceError as e:
                print(f"\n❌ {e}")
            break
        else:
            print("❌ Geçersiz seçim, tekrar deneyin.")


if __name__ == "__main__":
    main()
