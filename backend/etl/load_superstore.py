from pathlib import Path
from getpass import getpass

import pandas as pd
from sqlalchemy import create_engine, text


# ============================================================
# CONFIGURATION
# ============================================================

BASE_DIR = Path(__file__).resolve().parents[2]
DATA_FILE = BASE_DIR / "data" / "sample_-_superstore.xls"

DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "retailpulse"


# ============================================================
# DATABASE CONNECTION
# ============================================================

DB_PASSWORD = getpass("Enter PostgreSQL password: ")

DATABASE_URL = (
    f"postgresql+psycopg2://{DB_USER}:{DB_PASSWORD}"
    f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
)

engine = create_engine(DATABASE_URL)


# ============================================================
# LOAD SOURCE DATA
# ============================================================

print("\n========================================")
print("RetailPulse ETL")
print("========================================")

print("\nLoading dataset...")

df = pd.read_excel(DATA_FILE)

print(f"Source rows: {len(df):,}")


# ============================================================
# CLEAN COLUMN NAMES
# ============================================================

df.columns = [column.strip() for column in df.columns]


# ============================================================
# CONVERT DATA TYPES
# ============================================================

df["Order Date"] = pd.to_datetime(df["Order Date"])
df["Ship Date"] = pd.to_datetime(df["Ship Date"])

df["Sales"] = pd.to_numeric(df["Sales"])
df["Quantity"] = pd.to_numeric(df["Quantity"]).astype(int)
df["Discount"] = pd.to_numeric(df["Discount"])
df["Profit"] = pd.to_numeric(df["Profit"])


# ============================================================
# LOAD CUSTOMERS
# ============================================================

print("\n[1/5] Loading customers...")

customers = (
    df[
        [
            "Customer ID",
            "Customer Name",
            "Segment",
        ]
    ]
    .drop_duplicates(subset=["Customer ID"])
    .rename(
        columns={
            "Customer ID": "customer_id",
            "Customer Name": "customer_name",
            "Segment": "segment",
        }
    )
)

customers.to_sql(
    "customers",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Customers: {len(customers):,}")


# ============================================================
# LOAD LOCATIONS
# ============================================================

print("\n[2/5] Loading locations...")

locations = (
    df[
        [
            "Country/Region",
            "State/Province",
            "City",
            "Postal Code",
            "Region",
        ]
    ]
    .drop_duplicates()
    .rename(
        columns={
            "Country/Region": "country",
            "State/Province": "state_province",
            "City": "city",
            "Postal Code": "postal_code",
            "Region": "region",
        }
    )
)

locations.to_sql(
    "locations",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Locations: {len(locations):,}")


# ============================================================
# BUILD LOCATION LOOKUP
# ============================================================

location_lookup = pd.read_sql(
    """
    SELECT
        location_id,
        country,
        state_province,
        city,
        postal_code,
        region
    FROM locations
    """,
    engine,
)


# Normalize location fields so Excel/Pandas/PostgreSQL
# representations match consistently.

def normalize_value(value):
    if pd.isna(value):
        return ""

    value = str(value).strip()

    # Handle Excel-style numeric postal codes such as 9208.0
    if value.endswith(".0"):
        value = value[:-2]

    return value.lower()


df["_location_key"] = (
    df["Country/Region"].map(normalize_value)
    + "|"
    + df["State/Province"].map(normalize_value)
    + "|"
    + df["City"].map(normalize_value)
    + "|"
    + df["Postal Code"].map(normalize_value)
    + "|"
    + df["Region"].map(normalize_value)
)


location_lookup["_location_key"] = (
    location_lookup["country"].map(normalize_value)
    + "|"
    + location_lookup["state_province"].map(normalize_value)
    + "|"
    + location_lookup["city"].map(normalize_value)
    + "|"
    + location_lookup["postal_code"].map(normalize_value)
    + "|"
    + location_lookup["region"].map(normalize_value)
)


df = df.merge(
    location_lookup[
        ["location_id", "_location_key"]
    ],
    how="left",
    on="_location_key",
)


# ============================================================
# VALIDATE LOCATION MAPPING
# ============================================================

missing_locations = df["location_id"].isna().sum()

if missing_locations > 0:

    print(
        f"\nWARNING: {missing_locations} rows could not "
        "be mapped to a location."
    )

    print("\nExample unmatched rows:")

    print(
        df.loc[
            df["location_id"].isna(),
            [
                "Country/Region",
                "State/Province",
                "City",
                "Postal Code",
                "Region",
            ],
        ].head(10)
    )

    raise RuntimeError(
        f"{missing_locations} rows could not be mapped to a location."
    )

print("Location mapping: OK")

# ============================================================
# VALIDATE LOCATION MAPPING
# ============================================================

missing_locations = df["location_id"].isna().sum()

if missing_locations > 0:
    raise RuntimeError(
        f"{missing_locations} rows could not be mapped to a location."
    )


# ============================================================
# LOAD PRODUCTS
# ============================================================

print("\n[3/5] Loading products...")

products = (
    df[
        [
            "Product ID",
            "Product Name",
            "Category",
            "Sub-Category",
        ]
    ]
    .drop_duplicates(subset=["Product ID"])
    .rename(
        columns={
            "Product ID": "product_id",
            "Product Name": "product_name",
            "Category": "category",
            "Sub-Category": "sub_category",
        }
    )
)

products.to_sql(
    "products",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Products: {len(products):,}")


# ============================================================
# LOAD ORDERS
# ============================================================

print("\n[4/5] Loading orders...")

orders = (
    df[
        [
            "Order ID",
            "Customer ID",
            "location_id",
            "Order Date",
            "Ship Date",
            "Ship Mode",
        ]
    ]
    .drop_duplicates(subset=["Order ID"])
    .rename(
        columns={
            "Order ID": "order_id",
            "Customer ID": "customer_id",
            "Order Date": "order_date",
            "Ship Date": "ship_date",
            "Ship Mode": "ship_mode",
        }
    )
)

orders["order_date"] = orders["order_date"].dt.date
orders["ship_date"] = orders["ship_date"].dt.date

orders.to_sql(
    "orders",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Orders: {len(orders):,}")


# ============================================================
# LOAD ORDER ITEMS
# ============================================================

print("\n[5/5] Loading order items...")

order_items = (
    df[
        [
            "Row ID",
            "Order ID",
            "Product ID",
            "Sales",
            "Quantity",
            "Discount",
            "Profit",
        ]
    ]
    .rename(
        columns={
            "Row ID": "order_item_id",
            "Order ID": "order_id",
            "Product ID": "product_id",
            "Sales": "sales",
            "Quantity": "quantity",
            "Discount": "discount",
            "Profit": "profit",
        }
    )
)

order_items.to_sql(
    "order_items",
    engine,
    if_exists="append",
    index=False,
    method="multi",
)

print(f"Order items: {len(order_items):,}")


# ============================================================
# DATABASE VERIFICATION
# ============================================================

print("\n========================================")
print("DATABASE VERIFICATION")
print("========================================")

expected_counts = {
    "customers": len(customers),
    "locations": len(locations),
    "products": len(products),
    "orders": len(orders),
    "order_items": len(order_items),
}

with engine.connect() as connection:

    for table, expected in expected_counts.items():

        result = connection.execute(
            text(f"SELECT COUNT(*) FROM {table}")
        )

        actual = result.scalar()

        status = "OK" if actual == expected else "CHECK"

        print(
            f"{table:15} "
            f"expected={expected:>6,} "
            f"actual={actual:>6,} "
            f"[{status}]"
        )


print("\n========================================")
print("ETL COMPLETED SUCCESSFULLY")
print("========================================")