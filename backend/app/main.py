from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.db.database import engine, SessionLocal
from app.models.db_models import Base
from app.services.model_service import load_artifacts
from app.services.recommendation_service import seed_database
from app.routes import predict, features


@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- Startup ---
    # 1. Create DB tables
    Base.metadata.create_all(bind=engine)

    # 2. Seed recommendation data from CSVs (idempotent)
    db = SessionLocal()
    try:
        seed_database(db)
    finally:
        db.close()

    # 3. Load ML artifacts into memory once
    load_artifacts()

    yield
    # --- Shutdown (nothing special needed) ---


app = FastAPI(
    title="AI Disease Predictor API",
    description="Predict diseases from symptoms and get structured health recommendations.",
    version="1.0.0",
    lifespan=lifespan,
)

# Allow the React dev server (and any other origin in dev mode)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(predict.router, tags=["Prediction"])
app.include_router(features.router, tags=["Features"])


@app.get("/", tags=["Health"])
def root():
    return {"status": "ok", "message": "AI Disease Predictor API is running"}
