# StockFlow CLI

A Python-based CLI application for stock and sales management, built for small businesses.

Manage your products, track inventory, record sales, and generate reports — all from the terminal, with data persisted between sessions.

## Features

- Product management (add, delete, update, list, search)
- Stock tracking with low-stock alerts
- Sales management (stock is automatically deducted on each sale)
- Sales reports (total revenue, best-selling product, category breakdown, etc.)
- JSON data persistence (your data is saved and reloaded automatically)
- Robust error handling (the app never crashes on invalid input)

## Technologies Used

- Python
- OOP (Object-Oriented Programming)
- JSON
- Git
- GitHub

## Installation

Requires **Python 3.9+**. No external dependencies — only the standard library is used.

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/stockflow-cli.git
cd stockflow-cli
```

## Usage

Run the application from the project root:

```bash
python3 main.py
```

You'll be greeted with the main menu:

```
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
```

Navigate the numbered menus to manage products, record sales, check stock levels, and view reports. Data is loaded from `data/` on startup and saved automatically on exit (or manually via "Verileri Yedekle").

To run the manual test scenarios:

```bash
python3 test_manual.py
```

## Project Structure

```
stockflow-cli/
├── main.py                  # Entry point, main menu
├── product.py                # Product, PhysicalProduct, DigitalProduct classes
├── sale.py                   # Sale class
├── inventory_manager.py      # Product CRUD operations
├── sales_manager.py          # Sales operations
├── stock_manager.py          # Restocking / low-stock reports
├── reports_manager.py        # Reporting
├── persistence_manager.py    # JSON save/load
├── exceptions.py             # Custom exception classes
├── utils.py                  # Shared helper functions
├── test_manual.py            # Manual test scenarios
├── data/                     # JSON data files (not tracked in git)
├── .gitignore
└── README.md
```

## Screenshots

> Add terminal screenshots or GIFs here once the app is running, e.g. the main menu, a new sale flow, and a sales report.

```
✓ Sale successful.

New stock: 14
```

```
════════ SATIŞ RAPORU ════════

Toplam satış: 47

Toplam ciro:
₺84.750,50

En çok satan ürün:
Logitech G102
```
