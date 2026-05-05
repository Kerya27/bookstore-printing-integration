# 📚 Bookstore — Django Web System with Print Production Integration

A full-featured web system for selling printed books, built as a bachelor's diploma project. Combines a customer-facing bookstore with an admin panel and a print production workflow tracker — designed for small and mid-sized printing enterprises.

---

## ✨ Features

### Storefront
- Book catalog with category filtering, full-text search (Ukrainian-aware), and multi-parameter sorting
- Individual book pages with stock status
- Session-based cart with AJAX updates (no page reload)
- Guest checkout with automatic account creation and password delivery via email
- Personal cabinet with order history

### Admin Panel
- Dashboard with real-time stats: daily orders, pending count, monthly revenue
- Interactive Chart.js graphs with 7 / 30 / 90-day period switcher
- Full catalog management (add, edit, delete books and categories)
- Order management with inline status updates
- User list with slide-out detail panel (order history per customer)
- Excel export (`.xlsx`) with two sheets: order details + summary statistics

### Print Production Integration
- Every order automatically generates a linked `PrintJob` record
- 5-stage production workflow: `Pending → Prepress → Printing → Postpress → Done`
- Automatic timestamps when production stages change
- Production parameters per job: format, circulation, print method, paper type, binding type
- Visual production progress tracker in the admin order detail view

---

## 🛠 Tech Stack

| Layer | Technology |
|---|---|
| Backend | Python 3.12, Django 5.x |
| Database | SQLite (easily swappable to PostgreSQL) |
| Frontend | Bootstrap 5, Bootstrap Icons, Chart.js |
| Excel export | openpyxl |
| Auth | Django built-in + custom guest checkout flow |

---

## 🚀 Getting Started

```bash
# 1. Clone the repository
git clone https://github.com/Kerya27/bookstore-printing-integration.git
cd bookstore-printing-integration

# 2. Create and activate virtual environment
python -m venv .venv
.venv\Scripts\activate      # Windows
# source .venv/bin/activate  # macOS / Linux

# 3. Install dependencies
pip install -r requirements.txt

# 4. Apply migrations
python manage.py migrate

# 5. Create admin user
python manage.py createsuperuser

# 6. (Optional) Seed test data — 90 days of sample orders
python manage.py generate_orders

# 7. Run the development server
python manage.py runserver
```

Then open [http://127.0.0.1:8000](http://127.0.0.1:8000)  
Admin panel: [http://127.0.0.1:8000/admin-panel/](http://127.0.0.1:8000/admin-panel/)

---

## 📁 Project Structure

```
bookstore/
├── catalog/
│   ├── models.py          # Category, Book, Order, OrderItem, PrintJob, Profile
│   ├── views.py           # All views: storefront + custom admin panel
│   ├── urls.py
│   ├── context_processors.py
│   ├── management/
│   │   └── commands/
│   │       └── generate_orders.py
│   └── templates/
│       └── catalog/
│           ├── admin/     # Custom admin panel templates
│           └── ...        # Storefront templates
├── bookstore/
│   ├── settings.py
│   └── urls.py
├── media/                 # Uploaded book covers
├── requirements.txt
└── manage.py
```

---

## 📸 Screenshots

> Admin dashboard with revenue charts
> <img width="932" height="390" alt="image" src="https://github.com/user-attachments/assets/0892f365-eebe-4192-bddc-59bea1945751" />


> Order detail with production workflow tracker
> <img width="934" height="450" alt="image" src="https://github.com/user-attachments/assets/b2365442-87a2-4aa0-95ae-84d479fa05e3" />


> Storefront catalog with filters and search
> <img width="819" height="503" alt="image" src="https://github.com/user-attachments/assets/ac6d0361-b242-431b-b3d5-ffeb363e169b" />

> <img width="755" height="428" alt="image" src="https://github.com/user-attachments/assets/e59aff30-2dec-41c1-bd12-99f1618b8f78" />


---

## 🎓 About

Developed as a bachelor's diploma project at Kyiv Polytechnic Institute (KPI),  
specialty 186 — Publishing and Printing, 2025.

The system addresses a gap in existing bookstore platforms: none of them integrate with the internal production processes of a printing enterprise. This project bridges that gap by combining e-commerce functionality with a production management layer.
