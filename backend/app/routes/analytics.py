from fastapi import APIRouter, Query

from app.services.analytics import (
    get_overview,
    get_monthly_revenue,
    get_category_performance,
    get_regional_performance,
    get_filtered_dashboard,
    get_product_performance,
    get_customer_performance,
    get_sales_forecast,
    get_profit_anomalies,
)

router = APIRouter(
    prefix="/analytics",
    tags=["Analytics"],
)


@router.get("/overview")
def overview():
    return get_overview()


@router.get("/monthly-revenue")
def monthly_revenue():
    return get_monthly_revenue()


@router.get("/categories")
def categories():
    return get_category_performance()


@router.get("/regions")
def regions():
    return get_regional_performance()

@router.get("/dashboard")
def dashboard(
    date_from: str | None = Query(
        default=None,
        description="Start date, YYYY-MM-DD"
    ),
    date_to: str | None = Query(
        default=None,
        description="End date, YYYY-MM-DD"
    ),
    region: str | None = Query(
        default=None,
        description="Region filter"
    ),
    category: str | None = Query(
        default=None,
        description="Category filter"
    ),
    segment: str | None = Query(
        default=None,
        description="Customer segment filter"
    ),
):
    return get_filtered_dashboard(
        date_from=date_from,
        date_to=date_to,
        region=region,
        category=category,
        segment=segment,
    )
    
@router.get("/products")
def products(
    date_from: str = None,
    date_to: str = None,
    region: str = None,
    category: str = None,
    segment: str = None,
):
    return get_product_performance(
        date_from=date_from,
        date_to=date_to,
        region=region,
        category=category,
        segment=segment,
    )

@router.get("/customers")
def customers(
    date_from: str = None,
    date_to: str = None,
    region: str = None,
    category: str = None,
    segment: str = None,
):
    return get_customer_performance(
        date_from=date_from,
        date_to=date_to,
        region=region,
        category=category,
        segment=segment,
    )

@router.get("/forecast")
def forecast():
    return get_sales_forecast()


@router.get("/anomalies")
def anomalies():
    return get_profit_anomalies()