# RetailPulse

## Business Intelligence & Retail Analytics Platform

RetailPulse is an end-to-end retail business intelligence platform built using Python, PostgreSQL, FastAPI and React.

The platform transforms raw Superstore sales data into an interactive analytics dashboard for analyzing revenue, profitability, orders, products, customers and regional performance.

---

## Features

- Executive business overview
- Total revenue analysis
- Total profit analysis
- Order and unit analysis
- Profit margin calculation
- Interactive date filtering
- Regional filtering
- Category filtering
- Customer segment filtering
- Monthly revenue and profit analysis
- Category performance analysis
- Regional performance analysis
- Product intelligence
- Customer intelligence
- Revenue forecasting
- Profit anomaly detection
- PostgreSQL database
- Python ETL pipeline
- FastAPI REST APIs
- React dashboard
- Interactive charts

---

## Technology Stack

### Backend

- Python
- FastAPI
- SQLAlchemy
- PostgreSQL
- Pandas
- Psycopg2

### Frontend

- React
- Vite
- Recharts
- Lucide React
- CSS

### Database

- PostgreSQL

### Dataset

Superstore retail sales dataset containing:

- Orders
- Customers
- Products
- Locations
- Sales
- Quantity
- Discount
- Profit
- Order dates
- Shipping information

---

## Database Design

RetailPulse uses a normalized relational database containing five main tables.

### Customers

Stores customer information.

Fields:

- customer_id
- customer_name
- segment

### Locations

Stores geographic information.

Fields:

- location_id
- country
- state_province
- city
- postal_code
- region

### Products

Stores product information.

Fields:

- product_id
- product_name
- category
- sub_category

### Orders

Stores order-level information.

Fields:

- order_id
- customer_id
- location_id
- order_date
- ship_date
- ship_mode

### Order Items

Stores transaction-level sales information.

Fields:

- order_item_id
- order_id
- product_id
- sales
- quantity
- discount
- profit

---

## ETL Pipeline

The raw Superstore dataset is processed using a Python ETL pipeline.

The pipeline:

1. Reads the source dataset.
2. Cleans and validates the data.
3. Extracts unique customers.
4. Extracts unique locations.
5. Extracts unique products.
6. Extracts order-level information.
7. Extracts order-item transaction information.
8. Loads the transformed data into PostgreSQL.
9. Validates the loaded data.

---

## System Architecture

The application follows this architecture:

```text
Raw Superstore Dataset
          ↓
      Python ETL
          ↓
      PostgreSQL
          ↓
       SQLAlchemy
          ↓
        FastAPI
          ↓
       REST APIs
          ↓
        React
          ↓
 Interactive Dashboard

Analytics
Executive KPIs

The dashboard provides:

Total Revenue
Total Profit
Total Orders
Units Sold
Profit Margin

Profit margin is calculated as:

Profit Margin = Total Profit / Total Revenue × 100
Revenue Analysis

Monthly revenue and profit are aggregated from order transactions and displayed through interactive charts.

Product Intelligence

Products are ranked using revenue, profit and units sold to identify high-performing products.

Customer Intelligence

Customers are analyzed using:

Revenue
Profit
Orders
Units
Segment
Regional Analysis

Sales and profitability are analyzed across different business regions.

Revenue Forecasting

RetailPulse includes a simple three-month moving-average forecasting method.

The revenue from the most recent three months is averaged and used to estimate the following three months.

This provides a simple and explainable baseline forecast.

Profit Anomaly Detection

Monthly profit anomalies are identified using statistical Z-scores.

A month is flagged when the absolute Z-score reaches at least 2.

Anomalies are classified as:

Medium
High

This helps identify unusually strong or weak profit periods.

API Endpoints
GET /api/analytics/overview
GET /api/analytics/monthly-revenue
GET /api/analytics/categories
GET /api/analytics/regions
GET /api/analytics/dashboard
GET /api/analytics/products
GET /api/analytics/customers
GET /api/analytics/forecast
GET /api/analytics/anomalies
Running the Project
Backend

Open PowerShell:

cd D:\RetailPulse\backend
.\venv\Scripts\Activate.ps1
uvicorn main:app --reload

Backend:

http://127.0.0.1:8000

API documentation:

http://127.0.0.1:8000/docs
Frontend

Open another PowerShell window:

cd D:\RetailPulse\frontend
npm run dev

Frontend:

http://localhost:5173
Database Configuration

Database name:

retailpulse

Host:

localhost

Port:

5432

The PostgreSQL password is provided through the environment variable:

RETAILPULSE_DB_PASSWORD

The password should not be hard-coded in the source code.

Project Objective

The objective of RetailPulse is to demonstrate an end-to-end data analytics workflow:

Raw Data
   ↓
ETL
   ↓
PostgreSQL
   ↓
Analytics
   ↓
FastAPI
   ↓
React Dashboard
   ↓
Business Insights

The project combines data engineering, database management, backend API development and frontend data visualization into a single business intelligence platform.