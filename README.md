# Smart E-Commerce Platform

A full-stack e-commerce project with a React storefront, FastAPI customer API, and Django Admin. This repository is shared for mentor review; see **Project status** below for what is connected and what still needs configuration or implementation.

## Project structure

| Folder | Purpose |
| --- | --- |
| `customer-web/` | React, Vite, and Tailwind customer storefront |
| `customer-api/` | FastAPI routes, SQLAlchemy models, Auth0 token verification, and WebSockets |
| `admin/` | Django Admin for profiles, products, orders, payments, and reports |
| `database/schema.sql` | Initial shared PostgreSQL schema |
| `.env.example` | Names and placeholders for local environment variables; contains no credentials |

## Project status

| Area | Status |
| --- | --- |
| Public catalog | Home page shows all sample products and categories; catalog supports category, search, and sort filters |
| Customer API | Product, cart, order, payment, notification, WebSocket, and current-profile routes are present |
| Customer accounts | Auth0 integration is wired but needs a tenant, SPA client, and API audience configured |
| Admin records | Django models map to the same commerce tables used by FastAPI |
| Checkout and payment | Stripe test-session and webhook API routes exist; the storefront checkout is still sample UI and does not create real orders or payments |
| Product data | The current storefront catalog is sample data; it is not yet loaded from the products API |
| Supabase | Database configuration and SQL schema are provided; this repository does not include project credentials or create a Supabase project |
| Email and images | Email logs a safe development message by default; Supabase Storage upload is not yet wired into product management |

The project is a working development foundation, not production-ready. Configure external services and complete the remaining integrations before using it for real customers or payments. Do not use real payment data; Stripe must remain in test mode.

## Local setup on Windows

### 1. Configure environment

Copy `.env.example` to `.env` in the repository root, and copy `customer-web/.env.example` to `customer-web/.env`. Fill in the relevant values from your own Auth0, Supabase, and Stripe test accounts. Never commit either `.env` file.

For Auth0:

- Create an Auth0 **Single Page Application** and set `VITE_AUTH0_DOMAIN` and `VITE_AUTH0_CLIENT_ID` in `customer-web/.env`.
- Create/configure an Auth0 API audience. Set the same audience in the root `.env` (`AUTH0_API_AUDIENCE`) and `customer-web/.env` (`VITE_AUTH0_API_AUDIENCE`).
- Allow `http://localhost:5173` in the Auth0 application's **Allowed Callback URLs**, **Allowed Logout URLs**, and **Allowed Web Origins**.
- Enable the Auth0 database connection's sign-up option. Google and Facebook are available only if enabled and configured in Auth0.

For Supabase, set `SUPABASE_DATABASE_URL` in the root `.env`. Without it, FastAPI and Django share the local development database at `customer-api/smart_ecommerce.db`. To prepare a Supabase database, review and apply `database/schema.sql` to the intended project. The app does not connect to or modify a Supabase project until you configure its URL.

### 2. Start the customer API

Open a terminal in the repository and run:

```powershell
cd customer-api
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

API health: <http://localhost:8000/health>
Interactive API docs: <http://localhost:8000/docs>

### 3. Start the storefront

In a second terminal:

```powershell
cd customer-web
npm install
npm run dev
```

Storefront: <http://localhost:5173>

### 4. Create an admin login and start Django

In a third terminal:

```powershell
cd admin
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8001
```

Open <http://localhost:8001/admin/> and sign in using the username and password entered by `createsuperuser`. **There are no default Django admin credentials.** The Django superuser is an administrator account; customers sign in separately through Auth0.

## Viewing customer, order, and payment records

In Django Admin:

- **Users** lists customer profiles synchronized by the API after Auth0 sign-in.
- **Orders** lists recorded orders, customer emails, and order/payment statuses.
- **Payments** lists payment amounts, status, and Stripe references. Card numbers and security codes are not stored.

The API synchronizes the authenticated Auth0 profile at `GET /api/users/me`. Therefore, a customer must sign in through the configured storefront and the API and Django must point to the same database. Payments only appear after an order and payment record are created and a properly signed Stripe webhook is received.

**Current limitation:** Checkout in the storefront is not yet connected to the API. It uses sample presentation data and does not create a real order/payment. Customer, order, and payment tables may remain empty until the required Auth0/database setup is complete and the missing checkout integration is implemented.

## Security and configuration notes

- Keep `.env` files, credentials, service-role keys, database passwords, and Stripe secrets private.
- Use only Stripe test keys while developing. Never collect or store card numbers or CVC/CVV values in the app.
- The Django admin requires a Django superuser and should be deployed only behind HTTPS with production security settings.
- Auth0, Supabase, Stripe, email delivery, and storage require credentials and configuration from their respective providers; no credentials are included here.

## Verification commands

```powershell
cd customer-web
npm run build
npm run lint

cd ..\admin
python manage.py check
```
