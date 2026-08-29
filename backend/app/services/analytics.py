import os

from sqlalchemy import create_engine, text
from urllib.parse import quote_plus

DB_USER = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "retailpulse"


def create_db_engine():
    password = os.getenv("RETAILPULSE_DB_PASSWORD")

    if not password:
        raise RuntimeError("RETAILPULSE_DB_PASSWORD environment variable is not set.")

    encoded_password = quote_plus(password)

    database_url = (
        f"postgresql+psycopg2://"
        f"{DB_USER}:{encoded_password}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )

    return create_engine(database_url)


# ============================================================
# OVERVIEW
# ============================================================


def get_overview():
    engine = create_db_engine()

    query = text("""
        SELECT
            ROUND(SUM(oi.sales), 2) AS total_revenue,
            ROUND(SUM(oi.profit), 2) AS total_profit,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.quantity) AS total_units
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id;
    """)

    with engine.connect() as connection:
        result = connection.execute(query).mappings().first()

    total_revenue = float(result["total_revenue"] or 0)
    total_profit = float(result["total_profit"] or 0)

    profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

    return {
        "total_revenue": total_revenue,
        "total_profit": total_profit,
        "total_orders": int(result["total_orders"] or 0),
        "total_units": int(result["total_units"] or 0),
        "profit_margin": round(profit_margin, 2),
    }


# ============================================================
# MONTHLY REVENUE
# ============================================================


def get_monthly_revenue():
    engine = create_db_engine()

    query = text("""
        SELECT
            DATE_TRUNC('month', o.order_date) AS month,
            ROUND(SUM(oi.sales), 2) AS revenue,
            ROUND(SUM(oi.profit), 2) AS profit
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY DATE_TRUNC('month', o.order_date)
        ORDER BY month;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    return [
        {
            "month": row["month"].strftime("%Y-%m"),
            "revenue": float(row["revenue"] or 0),
            "profit": float(row["profit"] or 0),
        }
        for row in rows
    ]


# ============================================================
# CATEGORY PERFORMANCE
# ============================================================


def get_category_performance():
    engine = create_db_engine()

    query = text("""
        SELECT
            p.category,
            ROUND(SUM(oi.sales), 2) AS revenue,
            ROUND(SUM(oi.profit), 2) AS profit,
            SUM(oi.quantity) AS units
        FROM order_items oi
        JOIN products p
            ON oi.product_id = p.product_id
        GROUP BY p.category
        ORDER BY revenue DESC;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    return [
        {
            "category": row["category"],
            "revenue": float(row["revenue"] or 0),
            "profit": float(row["profit"] or 0),
            "units": int(row["units"] or 0),
        }
        for row in rows
    ]


# ============================================================
# REGIONAL PERFORMANCE
# ============================================================


def get_regional_performance():
    engine = create_db_engine()

    query = text("""
        SELECT
            l.region,
            ROUND(SUM(oi.sales), 2) AS revenue,
            ROUND(SUM(oi.profit), 2) AS profit,
            SUM(oi.quantity) AS units
        FROM order_items oi
        JOIN orders o
            ON oi.order_id = o.order_id
        JOIN locations l
            ON o.location_id = l.location_id
        GROUP BY l.region
        ORDER BY revenue DESC;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    return [
        {
            "region": row["region"],
            "revenue": float(row["revenue"] or 0),
            "profit": float(row["profit"] or 0),
            "units": int(row["units"] or 0),
        }
        for row in rows
    ]


# ============================================================
# FILTERED DASHBOARD
# ============================================================


def get_filtered_dashboard(
    date_from=None,
    date_to=None,
    region=None,
    category=None,
    segment=None,
):
    engine = create_db_engine()

    conditions = []
    params = {}

    if date_from:
        conditions.append("o.order_date >= :date_from")
        params["date_from"] = date_from

    if date_to:
        conditions.append("o.order_date <= :date_to")
        params["date_to"] = date_to

    if region:
        conditions.append("l.region = :region")
        params["region"] = region

    if category:
        conditions.append("p.category = :category")
        params["category"] = category

    if segment:
        conditions.append("c.segment = :segment")
        params["segment"] = segment

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    # ========================================================
    # OVERVIEW
    # ========================================================

    overview_query = text(f"""
        SELECT
            ROUND(SUM(oi.sales), 2) AS total_revenue,
            ROUND(SUM(oi.profit), 2) AS total_profit,
            COUNT(DISTINCT o.order_id) AS total_orders,
            SUM(oi.quantity) AS total_units

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause};
        """)

    # ========================================================
    # MONTHLY REVENUE
    # ========================================================

    monthly_query = text(f"""
        SELECT
            DATE_TRUNC(
                'month',
                o.order_date
            ) AS month,

            ROUND(
                SUM(oi.sales),
                2
            ) AS revenue,

            ROUND(
                SUM(oi.profit),
                2
            ) AS profit

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause}

        GROUP BY
            DATE_TRUNC(
                'month',
                o.order_date
            )

        ORDER BY month;
        """)

    # ========================================================
    # CATEGORY PERFORMANCE
    # ========================================================

    category_query = text(f"""
        SELECT
            p.category,

            ROUND(
                SUM(oi.sales),
                2
            ) AS revenue,

            ROUND(
                SUM(oi.profit),
                2
            ) AS profit,

            SUM(oi.quantity) AS units

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause}

        GROUP BY p.category

        ORDER BY revenue DESC;
        """)

    # ========================================================
    # REGIONAL PERFORMANCE
    # ========================================================

    region_query = text(f"""
        SELECT
            l.region,

            ROUND(
                SUM(oi.sales),
                2
            ) AS revenue,

            ROUND(
                SUM(oi.profit),
                2
            ) AS profit,

            SUM(oi.quantity) AS units

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause}

        GROUP BY l.region

        ORDER BY revenue DESC;
        """)

    # ========================================================
    # EXECUTE QUERIES
    # ========================================================

    with engine.connect() as connection:

        overview = connection.execute(overview_query, params).mappings().first()

        monthly_rows = connection.execute(monthly_query, params).mappings().all()

        category_rows = connection.execute(category_query, params).mappings().all()

        region_rows = connection.execute(region_query, params).mappings().all()

    # ========================================================
    # CALCULATE PROFIT MARGIN
    # ========================================================

    total_revenue = float(overview["total_revenue"] or 0)

    total_profit = float(overview["total_profit"] or 0)

    profit_margin = (total_profit / total_revenue) * 100 if total_revenue else 0

    # ========================================================
    # RETURN DASHBOARD DATA
    # ========================================================

    return {
        "filters": {
            "date_from": date_from,
            "date_to": date_to,
            "region": region,
            "category": category,
            "segment": segment,
        },
        "overview": {
            "total_revenue": total_revenue,
            "total_profit": total_profit,
            "total_orders": int(overview["total_orders"] or 0),
            "total_units": int(overview["total_units"] or 0),
            "profit_margin": round(profit_margin, 2),
        },
        "monthly_revenue": [
            {
                "month": row["month"].strftime("%Y-%m"),
                "revenue": float(row["revenue"] or 0),
                "profit": float(row["profit"] or 0),
            }
            for row in monthly_rows
        ],
        "categories": [
            {
                "category": row["category"],
                "revenue": float(row["revenue"] or 0),
                "profit": float(row["profit"] or 0),
                "units": int(row["units"] or 0),
            }
            for row in category_rows
        ],
        "regions": [
            {
                "region": row["region"],
                "revenue": float(row["revenue"] or 0),
                "profit": float(row["profit"] or 0),
                "units": int(row["units"] or 0),
            }
            for row in region_rows
        ],
    }


# ============================================================
# PRODUCT PERFORMANCE
# ============================================================


def get_product_performance(
    limit=10,
    date_from=None,
    date_to=None,
    region=None,
    category=None,
    segment=None,
):
    engine = create_db_engine()

    conditions = []
    params = {"limit": limit}

    if date_from:
        conditions.append("o.order_date >= :date_from")
        params["date_from"] = date_from

    if date_to:
        conditions.append("o.order_date <= :date_to")
        params["date_to"] = date_to

    if region:
        conditions.append("l.region = :region")
        params["region"] = region

    if category:
        conditions.append("p.category = :category")
        params["category"] = category

    if segment:
        conditions.append("c.segment = :segment")
        params["segment"] = segment

    where_clause = ""

    if conditions:
        where_clause = "WHERE " + " AND ".join(conditions)

    query = text(f"""
        SELECT
            p.product_id,
            p.product_name,
            p.category,

            ROUND(
                SUM(oi.sales),
                2
            ) AS revenue,

            ROUND(
                SUM(oi.profit),
                2
            ) AS profit,

            SUM(oi.quantity) AS units

        FROM order_items oi

        JOIN orders o
            ON oi.order_id = o.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN customers c
            ON o.customer_id = c.customer_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause}

        GROUP BY
            p.product_id,
            p.product_name,
            p.category

        ORDER BY revenue DESC

        LIMIT :limit;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query, params).mappings().all()

    return [
        {
            "product_id": row["product_id"],
            "product_name": row["product_name"],
            "category": row["category"],
            "revenue": float(row["revenue"] or 0),
            "profit": float(row["profit"] or 0),
            "units": int(row["units"] or 0),
        }
        for row in rows
    ]

# ============================================================
# CUSTOMER PERFORMANCE
# ============================================================

def get_customer_performance(
    limit=10,
    date_from=None,
    date_to=None,
    region=None,
    category=None,
    segment=None,
):
    engine = create_db_engine()

    conditions = []
    params = {"limit": limit}

    if date_from:
        conditions.append(
            "o.order_date >= :date_from"
        )
        params["date_from"] = date_from

    if date_to:
        conditions.append(
            "o.order_date <= :date_to"
        )
        params["date_to"] = date_to

    if region:
        conditions.append(
            "l.region = :region"
        )
        params["region"] = region

    if category:
        conditions.append(
            "p.category = :category"
        )
        params["category"] = category

    if segment:
        conditions.append(
            "c.segment = :segment"
        )
        params["segment"] = segment

    where_clause = ""

    if conditions:
        where_clause = (
            "WHERE " +
            " AND ".join(conditions)
        )

    query = text(f"""
        SELECT
            c.customer_id,
            c.customer_name,
            c.segment,

            COUNT(
                DISTINCT o.order_id
            ) AS orders,

            SUM(oi.quantity) AS units,

            ROUND(
                SUM(oi.sales),
                2
            ) AS revenue,

            ROUND(
                SUM(oi.profit),
                2
            ) AS profit

        FROM customers c

        JOIN orders o
            ON c.customer_id = o.customer_id

        JOIN order_items oi
            ON o.order_id = oi.order_id

        JOIN products p
            ON oi.product_id = p.product_id

        JOIN locations l
            ON o.location_id = l.location_id

        {where_clause}

        GROUP BY
            c.customer_id,
            c.customer_name,
            c.segment

        ORDER BY revenue DESC

        LIMIT :limit;
    """)

    with engine.connect() as connection:
        rows = connection.execute(
            query,
            params
        ).mappings().all()

    return [
        {
            "customer_id": row["customer_id"],
            "customer_name": row["customer_name"],
            "segment": row["segment"],
            "orders": int(
                row["orders"] or 0
            ),
            "units": int(
                row["units"] or 0
            ),
            "revenue": float(
                row["revenue"] or 0
            ),
            "profit": float(
                row["profit"] or 0
            ),
        }
        for row in rows
    ]

# ============================================================
# SALES FORECAST
# ============================================================


def get_sales_forecast():
    engine = create_db_engine()

    query = text("""
        SELECT
            DATE_TRUNC('month', o.order_date) AS month,
            ROUND(SUM(oi.sales), 2) AS revenue
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY DATE_TRUNC('month', o.order_date)
        ORDER BY month;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    history = [
        {
            "month": row["month"].strftime("%Y-%m"),
            "revenue": float(row["revenue"] or 0),
        }
        for row in rows
    ]

    if len(history) < 3:
        return {
            "history": history,
            "forecast": [],
        }

    # Simple moving-average forecast.
    # This is intentionally transparent and easy to explain.
    recent_values = [item["revenue"] for item in history[-3:]]

    average_revenue = sum(recent_values) / len(recent_values)

    last_month = rows[-1]["month"]

    from datetime import date

    year = last_month.year
    month = last_month.month

    forecast = []

    for i in range(1, 4):

        month += 1

        if month > 12:
            month = 1
            year += 1

        forecast.append(
            {
                "month": f"{year:04d}-{month:02d}",
                "revenue": round(average_revenue, 2),
            }
        )

    return {
        "history": history,
        "forecast": forecast,
    }


# ============================================================
# PROFIT ANOMALIES
# ============================================================


def get_profit_anomalies():
    engine = create_db_engine()

    query = text("""
        SELECT
            DATE_TRUNC('month', o.order_date) AS month,
            ROUND(SUM(oi.sales), 2) AS revenue,
            ROUND(SUM(oi.profit), 2) AS profit
        FROM orders o
        JOIN order_items oi
            ON o.order_id = oi.order_id
        GROUP BY DATE_TRUNC('month', o.order_date)
        ORDER BY month;
    """)

    with engine.connect() as connection:
        rows = connection.execute(query).mappings().all()

    values = [float(row["profit"] or 0) for row in rows]

    if len(values) < 3:
        return []

    mean_profit = sum(values) / len(values)

    variance = sum((value - mean_profit) ** 2 for value in values) / len(values)

    std_dev = variance**0.5

    anomalies = []

    for row in rows:

        profit = float(row["profit"] or 0)

        if std_dev == 0:
            z_score = 0
        else:
            z_score = (profit - mean_profit) / std_dev

        if abs(z_score) >= 2:

            anomalies.append(
                {
                    "month": row["month"].strftime("%Y-%m"),
                    "revenue": float(row["revenue"] or 0),
                    "profit": profit,
                    "z_score": round(z_score, 2),
                    "severity": "High" if abs(z_score) >= 3 else "Medium",
                }
            )

    return anomalies
