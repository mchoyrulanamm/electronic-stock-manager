# Stock Manager

Aplikasi manajemen stok komponen elektronik berbasis web. Dirancang untuk engineer elektronik yang perlu melacak stok resistor, IC, PCB, dan komponen lainnya dengan cepat.

## Fitur

- **Dashboard** — Statistik jumlah komponen, kategori, vendor, dan low stock alert
- **Components** — CRUD komponen dengan search by name, stock code, vcode, value, vendor
- **Categories** — Kelola kategori komponen
- **Vendors** — Kelola vendor/supplier komponen
- **Stock Movements** — Catat stok masuk/keluar via input stock code, stok otomatis terupdate
- **Export PDF** — Export laporan stock movement dengan filter tanggal
- **Low Stock Alert** — Tanda merah (stok < min) dan kuning (stok = min)
- **Autentikasi** — Login required + change password
- **Responsive** — Bootstrap 5, mobile friendly, sidebar collapse

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Flask (Python) |
| Database | SQLite via Flask-SQLAlchemy |
| ORM | SQLAlchemy |
| Frontend | Bootstrap 5 CDN, Jinja2, vanilla JS |
| Production | Gunicorn |
| PDF Export | fpdf2 |

## Cara Install & Jalankan

### Development

```bash
pip install -r requirements.txt
python app.py
```

### Production (Gunicorn)

```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 "app:create_app()"
```

Database dan user default akan terbuat otomatis saat pertama kali dijalankan.

## Default Login

| Username | Password |
|---|---|
| admin | admin |

Ganti password setelah login pertama melalui menu Admin > Change Password.

## Project Structure

```
├── app.py                  # Entry point Flask
├── config.py               # Konfigurasi DB
├── models.py               # Model SQLAlchemy
├── requirements.txt        # Dependencies
├── routes/
│   ├── __init__.py         # Decorator login_required
│   ├── auth.py             # Login / logout / change password
│   ├── components.py       # CRUD + search/filter komponen
│   ├── categories.py       # CRUD kategori
│   ├── vendors.py          # CRUD vendor
│   └── movements.py        # Stock movement + export PDF
├── templates/
│   ├── base.html           # Layout sidebar + header
│   ├── index.html          # Dashboard
│   ├── auth/
│   ├── components/
│   ├── categories/
│   ├── vendors/
│   └── movements/
├── static/
│   └── css/style.css
└── instance/
    └── inventory.db        # Auto-generated SQLite DB
```

## Lisensi

Creative Commons Attribution-NonCommercial (CC BY-NC).
