from fastapi import FastAPI
from app.routers import cafes, reviews
from app.core.errors import register_exception_handlers

app = FastAPI(
    title="CafeRate API",
    description="REST API untuk katalog kafe dan ulasan pengunjung.",
    version="1.0.0",
)

register_exception_handlers(app)
app.include_router(cafes.router, prefix="/api/v1")
app.include_router(reviews.router, prefix="/api/v1")


@app.get("/", tags=["Info"])
def root():
    return {"service": "CafeRate API", "version": "1.0.0", "docs": "/docs"}
