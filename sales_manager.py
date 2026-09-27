"""
sales_manager.py
------------------
StockFlow CLI - Satış Yönetimi.

Sale sınıfını ve ProductManager'ı kullanarak satış oluşturma, listeleme,
detay gösterme ve iptal etme işlemlerini yönetir. Satış yapıldığında
ilgili ürünün stoğu otomatik düşer; iptal edilince stok geri yüklenir.
"""

from sale import Sale
from inventory_manager import ProductManager
from exceptions import ProductNotFoundError, InsufficientStockError, InvalidQuantityError, SaleNotFoundError
from utils import input_float, input_int


class SaleManager:
    """Satışların tutulduğu ve yönetildiği sınıf."""

    def __init__(self, product_manager: ProductManager):
        self.product_manager = product_manager
        self.sales = {}          # {sale_id: Sale}
        self._next_id = 1

    def _generate_id(self):
        new_id = self._next_id
        self._next_id += 1
        return new_id

    def create_sale(self, product_id, quantity):
        product = self.product_manager.get_product(product_id)  # yoksa ProductNotFoundError

        if not isinstance(quantity, int) or quantity <= 0:
            raise InvalidQuantityError("Adet sıfırdan büyük bir tam sayı olmalı.")
        if quantity > product.stock:
            raise InsufficientStockError(
                f"Yetersiz stok. '{product.name}' için mevcut stok: {product.stock}"
            )

        sale_id = self._generate_id()
        sale = Sale(sale_id, product, quantity)
        product.stock -= quantity  # stok otomatik düşer
        self.sales[sale_id] = sale
        return sale

    def get_sale(self, sale_id):
        try:
            return self.sales[sale_id]
        except KeyError:
            raise SaleNotFoundError(f"{sale_id} ID'li satış bulunamadı.")

    def cancel_sale(self, sale_id):
        sale = self.get_sale(sale_id)
        sale.product.stock += sale.quantity  # stok geri yüklenir
        del self.sales[sale_id]
        return sale

    def list_sales(self):
        return list(self.sales.values())


# ==========================================================
#                    ARA YÜZ (CLI) FONKSİYONLARI
# ==========================================================

def new_sale_interactive(manager: SaleManager):
    print("\n--- Yeni Satış ---")
    try:
        product_id = input_int("Ürün ID: ")
        product = manager.product_manager.get_product(product_id)

        quantity = input_int("Adet: ")

        total = product.price * quantity
        print(f"\nÜrün: {product.name}")
        print(f"Birim fiyat: {product.price:.2f} TL")
        print(f"Adet: {quantity}")
        print(f"\nToplam: {total:.2f} TL")

        confirm = input("\nSatış gerçekleştirilsin mi? (E/H): ").strip().upper()
        if confirm != "E":
            print("\nSatış iptal edildi.")
            return

        sale = manager.create_sale(product_id, quantity)
        print(f"\n✓ Satış başarılı.\n\nYeni stok: {sale.product.stock}")

    except ProductNotFoundError as e:
        print(f"\n❌ {e}")
    except InsufficientStockError as e:
        print(f"\n❌ {e}")
    except InvalidQuantityError as e:
        print(f"\n❌ {e}")


def list_sales_interactive(manager: SaleManager):
    print("\n--- Satışlar ---")
    sales = manager.list_sales()
    if not sales:
        print("Kayıtlı satış yok.")
        return
    for sale in sales:
        print(
            f"\nSatış ID: {sale.sale_id} | {sale.product.name} | "
            f"Adet: {sale.quantity} | Toplam: {sale.total_amount:.2f} TL | "
            f"Tarih: {sale.date.strftime('%d.%m.%Y %H:%M')}"
        )


def sale_detail_interactive(manager: SaleManager):
    print("\n--- Satış Detayı ---")
    try:
        sale_id = input_int("Satış ID: ")
        sale = manager.get_sale(sale_id)
        print()
        print(sale)
    except SaleNotFoundError as e:
        print(f"\n❌ {e}")


def cancel_sale_interactive(manager: SaleManager):
    print("\n--- Satış İptal ---")
    try:
        sale_id = input_int("İptal edilecek satış ID: ")
        sale = manager.cancel_sale(sale_id)
        print(f"\n✓ Satış iptal edildi.\nStok geri yüklendi. Yeni stok: {sale.product.stock}")
    except SaleNotFoundError as e:
        print(f"\n❌ {e}")


def run_sales_menu(manager: SaleManager):
    """Satış Yönetimi alt menüsünü çalıştırır."""
    actions = {
        "1": new_sale_interactive,
        "2": list_sales_interactive,
        "3": sale_detail_interactive,
        "4": cancel_sale_interactive,
    }

    while True:
        print(
            "\nSatış Yönetimi\n\n"
            "1. Yeni satış\n"
            "2. Satışları listele\n"
            "3. Satış detayı\n"
            "4. Satış iptal\n"
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
    # Hızlı manuel test: önce bir ürün ekleyelim, sonra satış menüsünü çalıştıralım
    pm = ProductManager()
    pm.add_product("Logitech G102", "Elektronik", 799.99, 17, 5)
    sm = SaleManager(pm)
    run_sales_menu(sm)
