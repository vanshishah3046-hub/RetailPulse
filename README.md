# 📊 RetailPulse

### Retail Business Intelligence & Analytics Platform

RetailPulse is an end-to-end **Business Intelligence and Retail Analytics platform** that transforms raw Superstore transaction data into an interactive analytics dashboard.

The project combines **Python ETL, PostgreSQL, FastAPI and React** to provide business insights across revenue, profitability, customers, products, regions, forecasting and anomaly detection.

---

## ✨ Features

- 📈 Executive business overview
- 💰 Revenue and profit analysis
- 🛒 Order and unit analysis
- 📊 Profit margin calculation
- 📅 Date-based filtering
- 🌎 Regional performance analysis
- 🏷️ Category performance analysis
- 👥 Customer segment analysis
- 📦 Product intelligence
- 🧑‍💼 Customer intelligence
- 🔮 Revenue forecasting
- 🚨 Profit anomaly detection
- 🗄️ PostgreSQL relational database
- 🔄 Python ETL pipeline
- ⚡ FastAPI REST APIs
- ⚛️ React dashboard
- 📉 Interactive data visualizations

---

## 🏗️ System Architecture

```text
                 ┌──────────────────────┐
                 │  Superstore Dataset  │
                 │       (.xls)         │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     Python ETL       │
                 │ Pandas + Validation  │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │     PostgreSQL       │
                 │    RetailPulse DB    │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │       FastAPI        │
                 │     REST APIs        │
                 └──────────┬───────────┘
                            │
                            ▼
                 ┌──────────────────────┐
                 │        React         │
                 │ Analytics Dashboard  │
                 └──────────────────────┘

🛠️ Technology Stack
Backend
Python
FastAPI
SQLAlchemy
Pandas
Psycopg2
Database
PostgreSQL
Frontend
React
Vite
Recharts
Lucide React
CSS
Data Processing
Pandas
Python ETL pipeline
🗄️ Database Design

RetailPulse uses a normalized PostgreSQL database with five main tables.

Customers

Stores customer information.

customer_id
customer_name
segment
Locations

Stores geographic information.

location_id
country
state_province
city
postal_code
region
Products

Stores product information.

product_id
product_name
category
sub_category
Orders

Stores order-level information.

order_id
customer_id
location_id
order_date
ship_date
ship_mode
Order Items

Stores transaction-level sales information.

order_item_id
order_id
product_id
sales
quantity
discount
profit
🔄 ETL Pipeline

The Python ETL process converts the raw Superstore dataset into a structured relational database.

Pipeline
Raw Excel Dataset
       ↓
Data Loading
       ↓
Data Cleaning & Validation
       ↓
Customer Extraction
       ↓
Location Extraction
       ↓
Product Extraction
       ↓
Order Extraction
       ↓
Order Item Extraction
       ↓
PostgreSQL Loading
       ↓
Data Validation

The source dataset contains:

10,194 transaction rows
804 unique customers
5,111 unique orders
1,862 unique products
3 categories
17 sub-categories
4 regions
59 states/provinces
542 cities
📈 Analytics
Executive KPIs

RetailPulse calculates:

Total Revenue
Total Profit
Total Orders
Units Sold
Profit Margin

Profit margin:

Profit Margin = (Total Profit / Total Revenue) × 100
Revenue Analytics

Monthly revenue and profit are aggregated from transaction-level data and presented through interactive visualizations.

Category Analytics

Categories are compared using:

Revenue
Profit
Units Sold
Regional Analytics

Business performance is analyzed across the available geographic regions.

Product Intelligence

Products can be ranked using:

Revenue
Profit
Units Sold
Customer Intelligence

Customers are analyzed using:

Revenue
Profit
Orders
Units
Customer Segment
🔮 Revenue Forecasting

RetailPulse includes a baseline revenue forecasting system using a three-month moving average.

The latest three months of historical revenue are averaged to estimate the following three months.

Historical Revenue
       ↓
Latest 3 Months
       ↓
Moving Average
       ↓
Future Revenue Estimate

This approach provides a simple, transparent and explainable forecasting baseline.

🚨 Profit Anomaly Detection

RetailPulse identifies unusual monthly profit behavior using Z-score analysis.

A monthly profit value is evaluated against the distribution of historical monthly profits.

Months with an absolute Z-score of at least 2 are flagged as anomalies.

Monthly Profit
      ↓
Statistical Analysis
      ↓
Z-score
      ↓
Anomaly Detection
      ↓
Severity Classification

This helps identify unusually strong or weak profit periods.

🔌 API Endpoints
Endpoint	Purpose
GET /api/analytics/overview	Executive KPI overview
GET /api/analytics/monthly-revenue	Monthly revenue and profit
GET /api/analytics/categories	Category performance
GET /api/analytics/regions	Regional performance
GET /api/analytics/dashboard	Dashboard analytics
GET /api/analytics/products	Product intelligence
GET /api/analytics/customers	Customer intelligence
GET /api/analytics/forecast	Revenue forecasting
GET /api/analytics/anomalies	Profit anomaly detection

Interactive API documentation is available through FastAPI Swagger UI.

📁 Project Structure
RetailPulse/
│
├── backend/
│   ├── app/
│   │   ├── database/
│   │   ├── models/
│   │   ├── routes/
│   │   │   └── analytics.py
│   │   ├── services/
│   │   │   └── analytics.py
│   │   └── utils/
│   │
│   ├── etl/
│   │   └── load_superstore.py
│   │
│   ├── main.py
│   ├── requirements.txt
│   ├── .env.example
│   └── .gitignore
│
├── data/
│   └── sample_-_superstore.xls
│
├── database/
│
├── docs/
│
├── frontend/
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   ├── package.json
│   └── vite.config.js
│
└── README.md
🚀 Running Locally
1. Clone the repository
git clone https://github.com/vanshishah3046-hub/RetailPulse.git
cd RetailPulse
2. Backend Setup
cd backend
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt

Configure the PostgreSQL password using an environment variable:

RETAILPULSE_DB_PASSWORD=your_postgresql_password

Start FastAPI:

uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

Swagger documentation:

http://127.0.0.1:8000/docs
3. Frontend Setup

Open another terminal:

cd frontend
npm install
npm run dev

Vite will display the local frontend URL in the terminal.

🔐 Environment Variables

Sensitive credentials should not be committed to the repository.

Use:

RETAILPULSE_DB_PASSWORD=your_postgresql_password

The actual password should never be stored in source code or committed to GitHub.

🎯 Project Objective

RetailPulse demonstrates a complete data analytics workflow:

Raw Data
   ↓
ETL
   ↓
Database
   ↓
SQL Analytics
   ↓
REST API
   ↓
React Dashboard
   ↓
Business Intelligence

The project brings together data engineering, database management, backend development, statistical analysis and frontend visualization into a single retail analytics platform.

📌 Project Status

Status: Completed and functional

The current version includes the complete data pipeline, PostgreSQL database, FastAPI analytics APIs and React dashboard.

👩‍💻 Author

Vanshi Shah

RetailPulse was developed as an end-to-end data analytics and business intelligence project.
