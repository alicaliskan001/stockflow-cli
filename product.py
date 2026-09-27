"""
product.py
-----------
StockFlow CLI - Ürün (Product) sınıfı.

Bu modül, sistemdeki her bir ürünü temsil eden Product sınıfını içerir.
OOP konuları: __init__, instance attributes, @property, setter, __str__, __repr__
"""


class Product:
    """Bir stok kalemini (ürünü) temsil eder."""

    def __init__(self, product_id, name, category, price, stock, min_stock):
        self.product_id = product_id
        self.name = name
        self.category = category
        self.price = price          # setter üzerinden atanır (doğrulama yapılır)
        self.stock = stock          # setter üzerinden atanır (doğrulama yapılır)
        self.min_stock = min_stock  # setter üzerinden atanır (doğrulama yapılır)

    # ---------- price ----------
    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Fiyat sayısal bir değer olmalı.")
        if value < 0:
            raise ValueError("Fiyat negatif olamaz.")
        self._price = float(value)

    # ---------- stock ----------
    @property
    def stock(self):
        return self._stock

    @stock.setter
    def stock(self, value):
        if not isinstance(value, int):
            raise TypeError("Stok miktarı tam sayı olmalı.")
        if value < 0:
            raise ValueError("Stok miktarı negatif olamaz.")
        self._stock = value

    # ---------- min_stock ----------
    @property
    def min_stock(self):
        return self._min_stock

    @min_stock.setter
    def min_stock(self, value):
        if not isinstance(value, int):
            raise TypeError("Minimum stok tam sayı olmalı.")
        if value < 0:
            raise ValueError("Minimum stok negatif olamaz.")
        self._min_stock = value

    # ---------- yardımcı özellik ----------
    @property
    def is_low_stock(self):
        """Stok, minimum seviyenin altında veya eşit mi?"""
        return self.stock <= self.min_stock

    # ---------- dict dönüşümleri (ileride JSON için kullanılacak) ----------
    def to_dict(self):
        return {
            "product_type": "standard",
            "product_id": self.product_id,
            "name": self.name,
            "category": self.category,
            "price": self.price,
            "stock": self.stock,
            "min_stock": self.min_stock,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["product_id"],
            name=data["name"],
            category=data["category"],
            price=data["price"],
            stock=data["stock"],
            min_stock=data["min_stock"],
        )

    # ---------- yazdırma ----------
    def __str__(self):
        return (
            f"ID: {self.product_id}\n"
            f"Ürün: {self.name}\n"
            f"Kategori: {self.category}\n"
            f"Fiyat: {self.price:.2f} TL\n"
            f"Stok: {self.stock}\n"
            f"Minimum stok: {self.min_stock}"
        )

    def __repr__(self):
        return (
            f"Product(product_id={self.product_id!r}, name={self.name!r}, "
            f"category={self.category!r}, price={self.price!r}, "
            f"stock={self.stock!r}, min_stock={self.min_stock!r})"
        )


class PhysicalProduct(Product):
    """
    Fiziksel (elle tutulur, kargolanan) ürün.
    Örnek: Mouse, Klavye, Monitör, Laptop.
    """

    def __init__(self, product_id, name, category, price, stock, min_stock,
                 weight, location="Depo"):
        super().__init__(product_id, name, category, price, stock, min_stock)
        self.weight = weight      # kg cinsinden (setter doğrular)
        self.location = location  # raf/depo konumu

    # ---------- weight ----------
    @property
    def weight(self):
        return self._weight

    @weight.setter
    def weight(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Ağırlık sayısal bir değer olmalı.")
        if value < 0:
            raise ValueError("Ağırlık negatif olamaz.")
        self._weight = float(value)

    def to_dict(self):
        data = super().to_dict()
        data["product_type"] = "physical"
        data["weight"] = self.weight
        data["location"] = self.location
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["product_id"], name=data["name"], category=data["category"],
            price=data["price"], stock=data["stock"], min_stock=data["min_stock"],
            weight=data.get("weight", 0.0), location=data.get("location", "Depo"),
        )

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Tür: Fiziksel Ürün\n"
            f"Ağırlık: {self.weight} kg\n"
            f"Konum: {self.location}"
        )

    def __repr__(self):
        return (
            f"PhysicalProduct(product_id={self.product_id!r}, name={self.name!r}, "
            f"category={self.category!r}, price={self.price!r}, stock={self.stock!r}, "
            f"min_stock={self.min_stock!r}, weight={self.weight!r}, location={self.location!r})"
        )


class DigitalProduct(Product):
    """
    Dijital (indirilebilir/lisanslanan) ürün.
    Örnek: E-kitap, Online eğitim, Yazılım lisansı.
    """

    def __init__(self, product_id, name, category, price, stock, min_stock,
                 download_link, file_size_mb=0):
        super().__init__(product_id, name, category, price, stock, min_stock)
        self.download_link = download_link
        self.file_size_mb = file_size_mb  # setter doğrular

    # ---------- file_size_mb ----------
    @property
    def file_size_mb(self):
        return self._file_size_mb

    @file_size_mb.setter
    def file_size_mb(self, value):
        if not isinstance(value, (int, float)):
            raise TypeError("Dosya boyutu sayısal bir değer olmalı.")
        if value < 0:
            raise ValueError("Dosya boyutu negatif olamaz.")
        self._file_size_mb = float(value)

    def to_dict(self):
        data = super().to_dict()
        data["product_type"] = "digital"
        data["download_link"] = self.download_link
        data["file_size_mb"] = self.file_size_mb
        return data

    @classmethod
    def from_dict(cls, data):
        return cls(
            product_id=data["product_id"], name=data["name"], category=data["category"],
            price=data["price"], stock=data["stock"], min_stock=data["min_stock"],
            download_link=data.get("download_link", ""),
            file_size_mb=data.get("file_size_mb", 0.0),
        )

    def __str__(self):
        return (
            f"{super().__str__()}\n"
            f"Tür: Dijital Ürün\n"
            f"İndirme linki: {self.download_link}\n"
            f"Dosya boyutu: {self.file_size_mb} MB"
        )

    def __repr__(self):
        return (
            f"DigitalProduct(product_id={self.product_id!r}, name={self.name!r}, "
            f"category={self.category!r}, price={self.price!r}, stock={self.stock!r}, "
            f"min_stock={self.min_stock!r}, download_link={self.download_link!r}, "
            f"file_size_mb={self.file_size_mb!r})"
        )


# ---------- polymorphic factory: JSON'dan okurken doğru sınıfı seçer ----------
def product_from_dict(data):
    """product_type alanına bakarak doğru sınıfı (Product/PhysicalProduct/
    DigitalProduct) seçip nesneyi oluşturur. JSON'dan yükleme adımında kullanılacak."""
    product_type = data.get("product_type", "standard")
    if product_type == "physical":
        return PhysicalProduct.from_dict(data)
    elif product_type == "digital":
        return DigitalProduct.from_dict(data)
    return Product.from_dict(data)


if __name__ == "__main__":
    # Basit test
    p = Product(1001, "Logitech G102", "Elektronik", 799.99, 17, 5)
    print(p)
    print()
    print(repr(p))
    print("Düşük stok mu?", p.is_low_stock)

    print("\n" + "=" * 40 + "\n")

    physical = PhysicalProduct(1002, "Mekanik Klavye", "Elektronik", 1299.90, 10, 3,
                                weight=0.9, location="Raf A-3")
    print(physical)

    print("\n" + "=" * 40 + "\n")

    digital = DigitalProduct(1003, "Python 101 Eğitimi", "Yazılım", 249.00, 999, 0,
                              download_link="https://stockflow.local/downloads/py101",
                              file_size_mb=1450)
    print(digital)

    print("\n" + "=" * 40 + "\n")

    # Polymorphism: hepsi Product'tan türedi, hepsi Product listesinde tutulabilir
    urunler = [p, physical, digital]
    for u in urunler:
        print(f"[{type(u).__name__}] -> {u.name}")
