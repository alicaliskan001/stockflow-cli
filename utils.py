"""
utils.py
---------
StockFlow CLI - Ortak yardımcı fonksiyonlar.

Hem Ürün Yönetimi hem Satış Yönetimi ekranlarının kullandığı,
kullanıcıdan güvenli şekilde sayı almaya yarayan fonksiyonlar burada.
"""


def input_float(prompt):
    """Kullanıcıdan geçerli bir ondalık sayı alana kadar sorar (try/except)."""
    while True:
        try:
            return float(input(prompt).strip().replace(",", "."))
        except ValueError:
            print("❌ Geçersiz sayı, tekrar deneyin.")


def input_int(prompt):
    """Kullanıcıdan geçerli bir tam sayı alana kadar sorar (try/except)."""
    while True:
        try:
            return int(input(prompt).strip())
        except ValueError:
            print("❌ Geçersiz tam sayı, tekrar deneyin.")
