# AGENTS.md — Management Stock App

## Tech Stack

| Layer | Choice |
|---|---|
| Backend | Flask (Python) |
| Frontend | HTML + CSS + JS (vanilla, Jinja2 templates, Bootstrap 5 CDN) |
| Database | SQLite via Flask-SQLAlchemy |
| ORM | SQLAlchemy |

## How to Run

### Development
```bash
pip install -r requirements.txt
python app.py
```

### Production (with Gunicorn)
```bash
pip install -r requirements.txt
gunicorn -w 4 -b 0.0.0.0:5000 app:create_app()
```

Database auto-creates at `instance/inventory.db` on first run.

## Data Models

- **Vendor**: name, contact_person, email, phone, address, notes
- **Category**: name, description
- **Component**: name, stock_code, description, value, package, unit, stock_qty, min_stock, purchase_url, purchase_price, selling_price, category_id (FK), vendor_id (FK) — one vendor per component
- **StockMovement**: component_id (FK), quantity_change (+/-), movement_type ("in"/"out"), note

## Project Structure

```
├── app.py                  # Flask entry point
├── config.py               # DB config
├── models.py               # SQLAlchemy models
├── routes/
│   ├── vendors.py
│   ├── categories.py
│   ├── components.py       # includes search/filter
│   └── movements.py
├── templates/
│   ├── base.html           # layout with navbar + sidebar
│   └── ... (per-page templates)
├── static/css/, static/js/
└── instance/inventory.db   # auto-generated
```

## Conventions

- Blueprints for route organization
- Bootstrap 5 via CDN for UI
- Stock alert: highlight components where `stock_qty < min_stock` on dashboard
- StockMovement: positive quantity_change = stock in, negative = stock out
- Purchase URL stored as plain URL field on Component (one vendor per component)

## Session Context

This app manages electronic component inventory (resistors, ICs, PCBs, etc.) for an electronics engineer. Keep UI focused on quick stock lookups and updates.
