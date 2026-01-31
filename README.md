# HD-store Backend (Django + ERPNext)

Backend for an e-commerce store integrated with ERPNext.
- Catalog and stock are read live from ERPNext.
- Cart and Orders are managed in Django.
- Checkout creates an ERPNext Sales Order automatically.
- Sales Invoice is created manually by ERPNext staff (out of scope).

---

## Requirements
- Python 3.11+
- Virtualenv
- ERPNext instance reachable from backend (base URL + API key/secret)

---

## Setup (Local)

### 1) Create venv & install
```bash
python -m venv hdvenv
# Activate:
# Windows PowerShell:
#   .\hdvenv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2) Copy .env.example to .env and fill values:
```bash
copy .env.example .env
```

### 3) Database migrations
```bash
python manage.py migrate
```

### 4) Create admin user
```bash
python manage.py createsuperuser
```

### 5) Run server
```bash
python manage.py runserver
```

---

## ERPNext Configuration

### Required

Create an ERPNext API Key/Secret for a user.

Ensure these are set in `.env`:
- `ERPNEXT_BASE_URL`
- `ERPNEXT_API_KEY`
- `ERPNEXT_API_SECRET`

### Default Customer and Warehouse

Checkout creates a Sales Order in ERPNext and requires:
- `ERPNEXT_DEFAULT_CUSTOMER` exists in ERPNext (example: `Online Customer`)
- `ERPNEXT_DEFAULT_WAREHOUSE` exists and contains stock for items being purchased

---

## API Endpoints

### Health
- `GET /api/health/`

### Auth
- `POST /api/auth/register`
- `POST /api/auth/login`
- `GET /api/auth/me`

### Catalog (Public, ERPNext-backed)
- `GET /api/products/`
- `GET /api/products/{item_code}/`
- `GET /api/products/{item_code}/stock/`

### Cart (Auth required)

All cart endpoints are handled by a CartViewSet:
- `GET /api/cart/` (get current cart)
- `POST /api/cart/items/` (add item)
- `PATCH /api/cart/items/{id}/` (update qty)
- `DELETE /api/cart/items/{id}/` (delete item)

### Orders (Auth required)
- `POST /api/checkout/`
  - Creates Django Order
  - Creates ERPNext Sales Order automatically
  - Clears cart on success
- `GET /api/orders/` (my orders)
- `GET /api/orders/{order_id}/` (my order detail)

### Payments & Proof (Auth required)
- `POST /api/orders/{order_id}/vodafone-proof/`
  - Upload Vodafone Cash proof (multipart/form-data)
- `GET /api/orders/{order_id}/payments/`
  - List payment transactions for the order

### Staff Ops (Staff-only)
- `GET /api/staff/orders/` (list all orders; supports filters)
  - Query params:
    - `status=...`
    - `payment_status=...`
    - `q=...` (search in customer_name / phone / erp_sales_order_name)
- `GET /api/staff/orders/{order_id}/` (order detail)
- `POST /api/staff/orders/{order_id}/mark-paid/` (mark order as paid)
- `POST /api/staff/orders/{order_id}/status/` (update order status)

---

## Testing
Run tests:
```bash
pytest -q
```

## Notes / Business Rules

- Stock validation uses ERPNext `actual_qty`.
- Sales Order is created automatically at checkout.
- Sales Invoice is created manually by ERPNext staff.
- Vodafone Cash payments are verified manually by staff:
  - User uploads proof
  - Staff marks as paid
