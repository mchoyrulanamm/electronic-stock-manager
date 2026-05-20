# PANDUAN — Stock Manager

Dokumentasi lengkap aplikasi manajemen stok komponen elektronik.

## Daftar Isi

- [Arsitektur Aplikasi](#arsitektur-aplikasi)
- [Flow / Cara Kerja](#flow--cara-kerja)
- [Database Schema](#database-schema)
- [Cara Upload ke GitHub](#cara-upload-ke-github)
- [Project Structure](#project-structure)

---

## Arsitektur Aplikasi

Aplikasi ini menggunakan arsitektur **MVP (Model-View-Presenter)** sederhana:

```
Browser (Client)
     ↕ HTTP (Request/Response)
Flask (Routes / Blueprints)
     ↕
SQLAlchemy ORM
     ↕
SQLite Database (instance/inventory.db)
```

- **Model** → `models.py` (User, Component, Category, Vendor, StockMovement)
- **View** → `templates/` (Jinja2 HTML + Bootstrap 5)
- **Controller** → `routes/` (Blueprint per fitur)

Setiap request dari browser akan:

1. Dicek autentikasi oleh decorator `@login_required`
2. Diteruskan ke route handler yang sesuai
3. Route memproses data via SQLAlchemy
4. Hasil dirender ke template HTML
5. Dikirim kembali ke browser

---

## Flow / Cara Kerja

### 1. Autentikasi

```
User → Buka app → Redirect ke /login
  → Input username & password
  → POST /login
    → Cek User di DB
    → Cocokkan password (scrypt hash)
    → Simpan session (user_id, username)
    → Redirect ke Dashboard
```

Session disimpan di **cookie terenkripsi** (Flask session). Setiap route yang dilindungi mengecek ada/tidaknya `session['user_id']`. Kalau tidak ada, di-redirect ke `/login`.

### 2. Dashboard

```
/ (GET)
  → Hitung total components, categories, vendors
  → Query component dengan stock_qty < min_stock (low stock alert)
  → Query 10 movement terakhir
  → Render index.html
```

### 3. Components — CRUD + Search

```
/components/ (GET)             → List semua komponen (dengan filter)
/components/create (GET)       → Form tambah komponen
/components/create (POST)      → Simpan komponen baru ke DB
/components/<id>/edit (GET)    → Form edit komponen
/components/<id>/edit (POST)   → Update komponen
/components/<id>/delete (POST) → Hapus komponen
```

**Search & Filter**:

```
GET /components/?search=xxx&category_id=yyy&low_stock=1
  → Filter by name / stock_code / value / vendor.name (LIKE %search%)
  → Filter by category_id
  → Filter low stock only (stock_qty < min_stock)
```

**Highlight baris**:
- **Merah** → `stock_qty < min_stock`
- **Kuning** → `stock_qty == min_stock`

### 4. Categories — CRUD

Sederhana: create, read, update, delete kategori.

- Saat kategori dihapus, komponen di dalamnya menjadi `category_id = NULL`

### 5. Vendors — CRUD

Sederhana: create, read, update, delete vendor.

- Saat vendor dihapus, komponen di dalamnya menjadi `vendor_id = NULL`

### 6. Stock Movements

```
/movements/create (POST)
  → Input: component_id, movement_type (in/out), quantity, note
  → Hitung quantity_change:
      - "in"  → +quantity
      - "out" → -quantity
  → Update component.stock_qty
  → Simpan record ke stock_movements
  → Flash success message
```

**Aturan**: Tidak ada validasi stok minus — movement "out" tetap bisa dilakukan meskipun stok tidak mencukupi.

### 7. Change Password

```
/change-password (POST)
  → Validasi current_password cocok
  → Validasi new_password == confirm_password
  → Hash password baru (scrypt)
  → Update users.password_hash
  → Flash success
```

### 8. Session & Logout

```
/logout (GET)
  → session.clear()
  → Redirect ke /login
```

---

## Database Schema

### Entity Relationship

```
┌─────────────┐       ┌──────────────┐       ┌────────────┐
│   Vendor    │       │  Component   │       │  Category  │
├─────────────┤       ├──────────────┤       ├────────────┤
│ id (PK)     │──┐    │ id (PK)      │    ┌──│ id (PK)    │
│ name        │  │    │ name         │    │  │ name       │
│ contact     │  │    │ stock_code   │    │  │ description│
│ email       │  │    │ description  │    │  │ created_at │
│ phone       │  │    │ value        │    │  └────────────┘
│ address     │  │    │ package      │    │
│ notes       │  │    │ unit         │    │
│ created_at  │  │    │ stock_qty    │    │
└─────────────┘  │    │ min_stock    │    │
                 │    │ purchase_url │    │
                 │    │ purchase_price│   │
                 │    │ selling_price│   │
                 │    │ category_id──┼────┘
                 └────│ vendor_id    │
                      │ created_at   │
                      │ updated_at   │
                      └──────┬───────┘
                             │
                      ┌──────┴───────┐
                      │StockMovement │
                      ├──────────────┤
                      │ id (PK)      │
                      │ component_id │
                      │ quantity     │
                      │ type(in/out) │
                      │ note         │
                      │ created_at   │
                      └──────────────┘
```

### Tabel `users`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | |
| username | String(80), unique | |
| password_hash | String(256) | Hash scrypt |

### Tabel `vendors`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | |
| name | String(100) | Nama vendor |
| contact_person | String(100) | |
| email | String(100) | |
| phone | String(50) | |
| address | Text | |
| notes | Text | |
| created_at | DateTime | |

### Tabel `categories`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | |
| name | String(100), unique | Nama kategori |
| description | Text | |
| created_at | DateTime | |

### Tabel `components`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | |
| name | String(200) | Nama komponen |
| stock_code | String(50) | Kode stok internal |
| description | Text | |
| value | String(100) | Nilai (e.g. 10kΩ) |
| package | String(100) | Package (e.g. 0805) |
| unit | String(50) | pcs / meter / gram / liter |
| stock_qty | Integer | Jumlah stok saat ini |
| min_stock | Integer | Batas minimal stok |
| purchase_url | String(500) | Link pembelian |
| purchase_price | Float | Harga beli (Rp) |
| selling_price | Float | Harga jual (Rp) |
| category_id | Integer (FK → categories.id) | |
| vendor_id | Integer (FK → vendors.id) | Satu vendor per komponen |
| created_at | DateTime | |
| updated_at | DateTime | |

### Tabel `stock_movements`

| Kolom | Tipe | Keterangan |
|---|---|---|
| id | Integer (PK) | |
| component_id | Integer (FK → components.id) | |
| quantity_change | Integer | Positif = in, Negatif = out |
| movement_type | String(10) | "in" atau "out" |
| note | Text | Catatan movement |
| created_at | DateTime | |

---

## Cara Upload ke GitHub

### Pertama Kali Push

```bash
git init
git add .
git commit -m "Initial commit"
git branch -M main
git remote add origin https://github.com/username/nama-repo.git
git push -u origin main
```

### Update / Push Perubahan

```bash
git add .
git commit -m "Pesan perubahan"
git push
```

### Hapus File dari GitHub Tapi Simpan di Lokal

```bash
git rm --cached nama_file
git commit -m "Hapus nama_file dari repo"
git push
```

### .gitignore — File yang Tidak Ikut Terpush

```
instance/           # Database (inventory.db)
__pycache__/        # Cache Python
*.pyc               # Compiled Python
.vscode/            # Config VS Code
.env                # Environment variables
```

---

## Project Structure

```
├── app.py                  # Entry point Flask
├── config.py               # Konfigurasi DB & secret key
├── models.py               # Model SQLAlchemy (5 tabel)
├── requirements.txt        # Dependencies Python
├── .gitignore              # File yang diabaikan git
├── README.md               # Informasi singkat
├── PANDUAN.md              # Dokumentasi lengkap (file ini)
├── routes/
│   ├── __init__.py         # Decorator login_required
│   ├── auth.py             # Login / logout / change password
│   ├── components.py       # CRUD + search/filter komponen
│   ├── categories.py       # CRUD kategori
│   ├── vendors.py          # CRUD vendor
│   └── movements.py        # Stock movement in/out
├── templates/
│   ├── base.html           # Layout utama (sidebar + header + content)
│   ├── index.html          # Dashboard
│   ├── auth/
│   │   ├── login.html      # Halaman login
│   │   └── change_password.html
│   ├── components/
│   │   ├── list.html       # Tabel daftar komponen
│   │   └── form.html       # Form tambah/edit komponen
│   ├── categories/
│   │   ├── list.html
│   │   └── form.html
│   ├── vendors/
│   │   ├── list.html
│   │   └── form.html
│   └── movements/
│       ├── list.html
│       └── form.html
├── static/
│   └── css/
│       └── style.css       # Custom styles (green theme)
└── instance/
    └── inventory.db        # Auto-generated SQLite DB
```
