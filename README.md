# Smart E-Commerce Platform

This repository contains a small but complete e-commerce system split into three apps:

- `customer-web/` - React + Vite + Tailwind storefront
- `customer-api/` - FastAPI customer backend
- `admin/` - Django admin backend
- `database/schema.sql` - shared PostgreSQL schema for the main commerce data model

## Quick start

1. Copy `.env.example` to `.env` and fill in the values you want to use.
2. For frontend Auth0 sign-in, copy `customer-web/.env.example` to `customer-web/.env`, set the Auth0 domain/client ID/audience, and allow `http://localhost:5173` in the Auth0 application's Allowed Callback URLs, Allowed Logout URLs, and Allowed Web Origins.
3. Start the API:
   - `cd customer-api`
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1` (Windows PowerShell)
   - `pip install -r requirements.txt`
   - `uvicorn app.main:app --reload --host 0.0.0.0 --port 8000`
4. Start the frontend:
   - `cd customer-web`
   - `npm install`
   - `npm run dev -- --host 0.0.0.0`
5. Start the admin dashboard:
   - `cd admin`
   - `python -m venv .venv`
   - `.venv\Scripts\Activate.ps1`
   - `pip install -r requirements.txt`
   - `python manage.py migrate`
   - `python manage.py createsuperuser`
   - `python manage.py runserver 0.0.0.0:8001`

## Notes

- FastAPI and Django Admin use the same `SUPABASE_DATABASE_URL` when it is configured. Locally, both use `customer-api/smart_ecommerce.db`.
- The FastAPI API creates the shared commerce tables on startup. Django maps its read/write admin models to those same tables without trying to create or replace them.
- Auth0 and Stripe are expected to be configured in `.env` for production use.
- No secrets are committed to the repository.
- The customer API exposes the main storefront routes and the Django app handles the admin dashboard, analytics, and CSV exports.

## Viewing customer, order, and payment records

1. Configure Auth0, the shared database URL, and Stripe using `.env` and `customer-web/.env.example`. The Auth0 API audience in both files must match.
2. Start FastAPI and Django against the same database. After a customer signs in, the storefront calls `/api/users/me` to synchronize their Auth0 profile to the `users` table.
3. Start Django Admin and sign in with the Django staff superuser created by `python manage.py createsuperuser`.
4. Open `http://localhost:8001/admin/`:
   - **Users** shows synchronized customer profiles.
   - **Orders** shows each order with its customer email and statuses.
   - **Payments** shows amount, status, Stripe payment reference, and customer email.
5. Payment records appear only after an order is created and Stripe sends a verified webhook. Stripe card details are never stored.

The local storefront catalog/cart/order screens still use sample presentation data. Real customer profiles sync after Auth0 sign-in; the current checkout UI is not yet wired to create API orders or Stripe sessions. Payment rows therefore require an order/payment created through the API and a verified Stripe webhook. Configure Stripe test keys and a webhook endpoint before testing payments.
