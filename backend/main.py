from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routes.analytics import router as analytics_router

app = FastAPI(
    title="RetailPulse",
    version="1.0.0",
    description="Retail Business Intelligence & Predictive Analytics Platform",
)


# ==========================================
# CORS
# ==========================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "https://retailpulse-frontend.onrender.com",
],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(
    analytics_router,
    prefix="/api",
)
# ==========================================
# HEALTH CHECK
# ==========================================

@app.get("/")
def read_root():
    return {
        "message": "RetailPulse Backend is running",
        "status": "healthy",
    }


@app.get("/health")
def health_check():
    return {
        "status": "healthy",
    }