

class StockFlowError(Exception):
    """StockFlow CLI'daki tüm özel hataların temel sınıfı."""
    pass


class ProductNotFoundError(StockFlowError):
    """Belirtilen ID'ye sahip ürün bulunamadığında fırlatılır."""
    pass


class InvalidProductDataError(StockFlowError):
    """Ürün verisi (ad, kategori, fiyat, stok vb.) geçersiz olduğunda fırlatılır."""
    pass


class InsufficientStockError(StockFlowError):
    """Satış sırasında yeterli stok olmadığında fırlatılır."""
    pass


class InvalidQuantityError(StockFlowError):
    """Satış adedi geçersiz (sıfır veya negatif) olduğunda fırlatılır."""
    pass


class SaleNotFoundError(StockFlowError):
    """Belirtilen ID'ye sahip satış bulunamadığında fırlatılır."""
    pass


class DataPersistenceError(StockFlowError):
    """JSON dosyalarına kaydetme/yükleme sırasında bir sorun oluştuğunda fırlatılır."""
    pass
