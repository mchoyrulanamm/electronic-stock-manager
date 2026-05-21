# Stock Manager

Aplikasi manajemen stok komponen elektronik berbasis web. Dirancang untuk engineer elektronik yang perlu melacak stok resistor, IC, PCB, dan komponen lainnya dengan cepat.

## Fitur

- **Dashboard** — Stat cards (total komponen, kategori, vendor), low stock alert, dan 10 movement terbaru
- **Components** — CRUD komponen dengan search by name, stock code, vcode, value, vendor
- **Categories** — Kelola kategori komponen
- **Vendors** — Kelola vendor/supplier komponen
- **Stock Movements** — Catat stok masuk/keluar via input stock code, stok otomatis terupdate
- **Export PDF** — Export laporan stock movement dengan filter tanggal
- **Low Stock Alert** — Tanda merah (stok < min) dan kuning (stok = min)
- **Autentikasi** — Login required + change password
- **Responsive** — Bootstrap 5 + Bootstrap Icons, mobile friendly, sidebar collapse
- **Global Search** — Quick search komponen dari header

## Tech Stack

| Layer | Tech |
|---|---|
| Backend | Flask (Python) |
| Database | SQLite via Flask-SQLAlchemy |
| ORM | SQLAlchemy |
| Frontend | Bootstrap 5 CDN + Bootstrap Icons, Jinja2, vanilla JS |
| Production | Gunicorn |
| PDF Export | fpdf2 |

## Environment Variables

| Variable | Default | Keterangan |
|---|---|---|
| `SECRET_KEY` | `dev-secret-key` | Flask session secret key |
| `DATABASE_URL` | `sqlite:///instance/inventory.db` | Database URI |

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
├── config.py               # Konfigurasi DB & SECRET_KEY
├── models.py               # Model SQLAlchemy (5 tabel)
├── requirements.txt        # Dependencies Python
├── .gitignore
├── routes/
│   ├── __init__.py         # Decorator login_required
│   ├── auth.py             # Login / logout / change password
│   ├── components.py       # CRUD + search/filter komponen
│   ├── categories.py       # CRUD kategori
│   ├── vendors.py          # CRUD vendor
│   └── movements.py        # Stock movement + export PDF
├── templates/
│   ├── base.html           # Layout sidebar + header + global search
│   ├── index.html          # Dashboard
│   ├── auth/
│   │   ├── login.html
│   │   └── change_password.html
│   ├── components/
│   │   ├── list.html
│   │   └── form.html
│   ├── categories/
│   │   ├── list.html
│   │   └── form.html
│   ├── vendors/
│   │   ├── list.html
│   │   └── form.html
│   ├── movements/
│   │   ├── list.html
│   │   └── form.html
│   └── partials/          # Partial templates
├── static/
│   ├── css/
│   │   └── style.css       # Green theme custom CSS
│   └── js/                 # Custom JavaScript
└── instance/
    └── inventory.db        # Auto-generated SQLite DB
```

## Lisensi

Creative Commons Attribution-NonCommercial (CC BY-NC).
