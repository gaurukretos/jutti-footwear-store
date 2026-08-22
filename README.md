# Dabi Jutti House — Footwear E-Commerce

Modern Django website for retail & wholesale footwear — Rajasthani Juttis, Mojaris, Kolhapuri, and more for Men, Women & Kids.

## Features

- **Categories:** Men, Women, Child
- **Styles:** Rajasthani Jutti, Punjabi Jutti, Mojari, Kolhapuri, Wedding Jutti, Sandals, Sports
- **Retail shopping** with cart & checkout
- **Wholesale mode** with bulk pricing & minimum quantity rules
- **Wholesale inquiry form** for custom bulk quotes
- **PostgreSQL** database with dummy seed data
- **Django Admin** for managing products & orders

## Quick Start

### 1. Start PostgreSQL (Docker)

```bash
docker compose up -d
```

### 2. Install Python dependencies

```bash
pip install -r requirements.txt
```

### 3. Run migrations & seed data

```bash
python manage.py migrate
python manage.py seed_data
python manage.py createsuperuser
```

### 4. Run the development server

```bash
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

Admin panel: **http://127.0.0.1:8000/admin/**

## Project Structure

```
jutti-footwear-store/
├── config/          # Django settings
├── shop/            # Main app (models, views, cart)
├── templates/       # HTML templates
├── static/          # CSS
├── docker-compose.yml
└── requirements.txt
```

## Wholesale vs Retail

Use the **Retail / Wholesale** toggle in the header to switch pricing mode. In wholesale mode, minimum order quantities apply per product.
