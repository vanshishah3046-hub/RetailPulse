# 📊 RetailPulse

### Retail Business Intelligence & Analytics Platform

RetailPulse is an end-to-end **Business Intelligence and Retail Analytics platform** that transforms raw Superstore transaction data into an interactive analytics dashboard.

The project combines **Python ETL, PostgreSQL, FastAPI, SQLAlchemy, and React** to provide business insights across revenue, profitability, customers, products, regions, forecasting, and anomaly detection.

---

## ✨ Features

- 📈 Executive business overview
- 💰 Revenue and profit analysis
- 🛒 Order and unit analysis
- 📊 Profit margin calculation
- 📅 Date range filtering
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
                    │        (.xls)        │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │      Python ETL      │
                    │   Pandas + Cleaning  │
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
                    │      SQLAlchemy      │
                    │   Database Access    │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │       FastAPI        │
                    │      REST APIs       │
                    └──────────┬───────────┘
                               │
                               ▼
                    ┌──────────────────────┐
                    │        React         │
                    │  Analytics Dashboard │
                    └──────────────────────┘
```

---

## 🛠️ Technology Stack

### Backend

- **Python**
- **FastAPI**
- **SQLAlchemy**
- **Pandas**
- **Psycopg2**

### Database

- **PostgreSQL**

### Frontend

- **React**
- **Vite**
- **Recharts**
- **Lucide React**
- **CSS**

### Data Processing

- **Pandas**
- Python-based ETL pipeline

---

## 🗄️ Database Design

RetailPulse uses a normalized PostgreSQL database consisting of five main tables.

### 1. Customers

Stores customer information.

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `customer_name` | Customer name |
| `segment` | Customer segment |

---

### 2. Locations

Stores geographic information.

| Column | Description |
|---|---|
| `location_id` | Unique location identifier |
| `country` | Country |
| `state_province` | State or province |
| `city` | City |
| `postal_code` | Postal code |
| `region` | Business region |

---

### 3. Products

Stores product information.

| Column | Description |
|---|---|
| `product_id` | Unique product identifier |
| `product_name` | Product name |
| `category` | Product category |
| `sub_category` | Product sub-category |

---

### 4. Orders

Stores order-level information.

| Column | Description |
|---|---|
| `order_id` | Unique order identifier |
| `customer_id` | Associated customer |
| `location_id` | Associated location |
| `order_date` | Date the order was placed |
| `ship_date` | Date the order was shipped |
| `ship_mode` | Shipping method |

---

### 5. Order Items

Stores transaction-level sales information.

| Column | Description |
|---|---|
| `order_item_id` | Unique transaction identifier |
| `order_id` | Associated order |
| `product_id` | Associated product |
| `sales` | Sales amount |
| `quantity` | Units sold |
| `discount` | Discount applied |
| `profit` | Profit generated |

---

## 🔄 ETL Pipeline

The Python ETL pipeline transforms the raw Superstore dataset into structured relational data.

### Pipeline

```text
Raw Excel Dataset
        │
        ▼
Data Loading
        │
        ▼
Data Cleaning & Validation
        │
        ▼
Customer Extraction
        │
        ▼
Location Extraction
        │
        ▼
Product Extraction
        │
        ▼
Order Extraction
        │
        ▼
Order Item Extraction
        │
        ▼
PostgreSQL Loading
        │
        ▼
Data Validation
```

### Dataset Statistics

The source dataset contains:

| Metric | Count |
|---|---:|
| Transaction Rows | 10,194 |
| Unique Customers | 804 |
| Unique Orders | 5,111 |
| Unique Products | 1,862 |
| Categories | 3 |
| Sub-Categories | 17 |
| Regions | 4 |
| States / Provinces | 59 |
| Cities | 542 |

---

## 📈 Analytics

### Executive KPIs

The dashboard provides the following key performance indicators:

- **Total Revenue**
- **Total Profit**
- **Total Orders**
- **Units Sold**
- **Profit Margin**

### Profit Margin

```text
Profit Margin = (Total Profit / Total Revenue) × 100
```

---

### 📊 Revenue Analytics

Monthly revenue and profit are aggregated from transaction-level data and presented through interactive visualizations.

This allows users to identify changes in business performance over time.

---

### 🏷️ Category Analytics

Product categories are compared using:

- Revenue
- Profit
- Units Sold

This provides an overview of which categories contribute most to overall business performance.

---

### 🌎 Regional Analytics

Sales and profitability are analyzed across the available business regions.

This helps identify geographic differences in performance.

---

### 📦 Product Intelligence

Products can be analyzed and ranked using:

- Revenue
- Profit
- Units Sold

This helps identify high-performing products.

---

### 👥 Customer Intelligence

Customers are analyzed using:

- Revenue
- Profit
- Orders
- Units
- Customer Segment

This helps identify valuable customers and understand customer behavior.

---

## 🔮 Revenue Forecasting

RetailPulse includes a baseline revenue forecasting system based on a **three-month moving average**.

The latest three months of historical revenue are averaged to estimate the following three months.

### Forecasting Process

```text
Historical Revenue
        │
        ▼
Latest Three Months
        │
        ▼
Three-Month Moving Average
        │
        ▼
Future Revenue Estimate
```

The approach is intentionally simple and explainable, making it suitable as a transparent forecasting baseline.

---

## 🚨 Profit Anomaly Detection

RetailPulse identifies unusual monthly profit behavior using **Z-score analysis**.

A monthly profit value is compared against the historical distribution of monthly profits.

Months with an absolute Z-score of at least **2** are flagged as anomalies.

### Detection Process

```text
Monthly Profit
      │
      ▼
Statistical Analysis
      │
      ▼
Z-score Calculation
      │
      ▼
Anomaly Detection
      │
      ▼
Severity Classification
```

Anomalies are classified into severity levels such as:

- **Medium**
- **High**

This helps identify unusually strong or weak profit periods.

---

## 🔌 API Endpoints

RetailPulse exposes analytics through FastAPI REST endpoints.

| Method | Endpoint | Purpose |
|---|---|---|
| `GET` | `/api/analytics/overview` | Executive KPI overview |
| `GET` | `/api/analytics/monthly-revenue` | Monthly revenue and profit |
| `GET` | `/api/analytics/categories` | Category performance |
| `GET` | `/api/analytics/regions` | Regional performance |
| `GET` | `/api/analytics/dashboard` | Combined dashboard analytics |
| `GET` | `/api/analytics/products` | Product intelligence |
| `GET` | `/api/analytics/customers` | Customer intelligence |
| `GET` | `/api/analytics/forecast` | Revenue forecasting |
| `GET` | `/api/analytics/anomalies` | Profit anomaly detection |

### API Documentation

FastAPI provides interactive Swagger documentation at:

```text
http://127.0.0.1:8000/docs
```

---

## 📁 Project Structure

```text
RetailPulse/
│
├── backend/
│   │
│   ├── app/
│   │   ├── database/
│   │   │   └── __init__.py
│   │   │
│   │   ├── models/
│   │   │   └── __init__.py
│   │   │
│   │   ├── routes/
│   │   │   ├── __init__.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── services/
│   │   │   ├── __init__.py
│   │   │   └── analytics.py
│   │   │
│   │   ├── utils/
│   │   │   └── __init__.py
│   │   │
│   │   └── __init__.py
│   │
│   ├── etl/
│   │   ├── __init__.py
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
│   │
│   ├── public/
│   ├── src/
│   │   ├── assets/
│   │   ├── App.jsx
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.jsx
│   │
│   ├── package.json
│   ├── package-lock.json
│   ├── vite.config.js
│   └── eslint.config.js
│
└── README.md
```

---

## 🚀 Running the Project Locally

### Prerequisites

Make sure the following are installed:

- Python
- PostgreSQL
- Node.js
- npm

---

### 1. Clone the Repository

```bash
git clone https://github.com/vanshishah3046-hub/RetailPulse.git
cd RetailPulse
```

---

### 2. Backend Setup

Navigate to the backend:

```powershell
cd backend
```

Create a virtual environment:

```powershell
python -m venv venv
```

Activate it:

```powershell
.\venv\Scripts\Activate.ps1
```

Install dependencies:

```powershell
pip install -r requirements.txt
```

---

### 3. Configure PostgreSQL

RetailPulse uses:

```text
Database: retailpulse
Host: localhost
Port: 5432
```

Set the PostgreSQL password using the environment variable:

```text
RETAILPULSE_DB_PASSWORD=your_postgresql_password
```

Do not hard-code the PostgreSQL password in the source code.

---

### 4. Start the FastAPI Backend

From the `backend` directory:

```powershell
uvicorn main:app --reload
```

Backend:

```text
http://127.0.0.1:8000
```

Swagger API documentation:

```text
http://127.0.0.1:8000/docs
```

---

### 5. Start the React Frontend

Open another terminal:

```powershell
cd frontend
```

Install frontend dependencies:

```powershell
npm install
```

Start the development server:

```powershell
npm run dev
```

Vite will display the local frontend URL in the terminal.

---

## 🔐 Environment Variables

Sensitive credentials should never be committed to GitHub.

RetailPulse uses:

```text
RETAILPULSE_DB_PASSWORD=your_postgresql_password
```

The repository contains `.env.example` as a safe configuration template.

The actual `.env` file should remain local.

---

## 📌 Project Workflow

The complete RetailPulse workflow is:

```text
                 RAW DATA
                    │
                    ▼
              PYTHON ETL
                    │
                    ▼
              POSTGRESQL
                    │
                    ▼
            ANALYTICS QUERIES
                    │
                    ▼
                FASTAPI
                    │
                    ▼
              REST APIs
                    │
                    ▼
                REACT
                    │
                    ▼
        INTERACTIVE DASHBOARD
                    │
                    ▼
          BUSINESS INSIGHTS
```

---

## 🎯 Project Objective

The objective of RetailPulse is to demonstrate a complete end-to-end data analytics and business intelligence workflow.

The project integrates:

- Data processing
- ETL
- Relational database design
- SQL analytics
- REST API development
- Statistical analysis
- Forecasting
- Anomaly detection
- Interactive data visualization

into a single retail analytics platform.

---

## 📊 Project Status

**Completed and functional.**

The current version includes:

- Complete ETL pipeline
- PostgreSQL database
- FastAPI backend
- Analytics REST APIs
- React dashboard
- Interactive filtering
- Product intelligence
- Customer intelligence
- Revenue forecasting
- Profit anomaly detection

---

## 👩‍💻 Author

**Vanshi Shah**

RetailPulse is an end-to-end retail analytics and business intelligence project combining data engineering, backend development, database management, statistical analysis, and frontend visualization.
