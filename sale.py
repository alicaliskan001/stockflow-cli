"""
sale.py
--------
StockFlow CLI - Sale (Satış) sınıfı.

Product ile Sale birlikte çalışır: bir Sale nesnesi, hangi Product'ın
kaç adet satıldığını ve ne zaman satıldığını tutar.
"""

from datetime import datetime


class Sale:
    """Tek bir satış işlemini temsil eder."""

    def __init__(self, sale_id, product, quantity, date=None):
        self.sale_id = sale_id
        self.product = product      # bir Product (veya alt sınıfı) nesnesi
        self.quantity = quantity    # setter doğrular (pozitif tam sayı)
        self.date = date or datetime.now()

    # ---------- quantity ----------
    @property
    def quantity(self):
        return self._quantity

    @quantity.setter
    def quantity(self, value):
        if not isinstance(value, int):
            raise TypeError("Adet tam sayı olmalı.")
        if value <= 0:
            raise ValueError("Adet sıfırdan büyük olmalı.")
        self._quantity = value

    # ---------- hesaplanan alanlar ----------
    @property
    def unit_price(self):
        return self.product.price

    @property
    def total_amount(self):
        return self.product.price * self.quantity

    # ---------- dict dönüşümü (JSON için) ----------
    def to_dict(self):
        return {
            "sale_id": self.sale_id,
            "product_id": self.product.product_id,
            "product_name": self.product.name,
            "unit_price": self.unit_price,
            "quantity": self.quantity,
            "total_amount": self.total_amount,
            "date": self.date.strftime("%Y-%m-%d %H:%M:%S"),
        }

    # ---------- yazdırma ----------
    def __str__(self):
        return (
            f"Satış ID: {self.sale_id}\n"
            f"Ürün: {self.product.name}\n"
            f"Birim fiyat: {self.unit_price:.2f} TL\n"
            f"Adet: {self.quantity}\n"
            f"Tarih: {self.date.strftime('%d.%m.%Y %H:%M')}\n"
            f"\nToplam: {self.total_amount:.2f} TL"
        )

    def __repr__(self):
        return (
            f"Sale(sale_id={self.sale_id!r}, product_id={self.product.product_id!r}, "
            f"quantity={self.quantity!r}, total_amount={self.total_amount!r}, "
            f"date={self.date!r})"
        )
