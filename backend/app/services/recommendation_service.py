import os
import pandas as pd
from sqlalchemy.orm import Session
from app.models.db_models import Disease, Precaution, Medication, Workout, Diet
from dotenv import load_dotenv

load_dotenv()


def _datasets_dir() -> str:
    base = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    return os.path.join(base, os.getenv("DATASETS_DIR", "datasets"))


def _clean(val) -> str | None:
    """Strip whitespace and return None if NaN or empty."""
    if pd.isna(val):
        return None
    s = str(val).strip()
    return s if s else None


def seed_database(db: Session):
    """Populate DB from CSVs if tables are empty — idempotent."""
    if db.query(Disease).count() > 0:
        print("[Seed] Database already seeded, skipping.")
        return

    print("[Seed] Seeding database from CSVs...")
    d = _datasets_dir()

    prec_df = pd.read_csv(os.path.join(d, "precautions_df.csv"))
    med_df  = pd.read_csv(os.path.join(d, "medications.csv"))
    wrk_df  = pd.read_csv(os.path.join(d, "workout_df.csv"))
    diet_df = pd.read_csv(os.path.join(d, "diets.csv"))

    # Strip column name spaces
    prec_df.columns = prec_df.columns.str.strip()
    med_df.columns  = med_df.columns.str.strip()
    wrk_df.columns  = wrk_df.columns.str.strip()
    diet_df.columns = diet_df.columns.str.strip()

    disease_map: dict[str, Disease] = {}

    def get_or_create(name: str) -> Disease:
        key = name.strip().lower()
        if key not in disease_map:
            d_obj = Disease(name=name.strip())
            db.add(d_obj)
            db.flush()
            disease_map[key] = d_obj
        return disease_map[key]

    # --- Precautions ---
    prec_cols = [c for c in prec_df.columns if c.startswith("Precaution_")]
    for _, row in prec_df.iterrows():
        dis = get_or_create(str(row["Disease"]))
        for col in prec_cols:
            val = _clean(row.get(col))
            if val:
                db.add(Precaution(disease_id=dis.id, text=val))

    # --- Medications ---
    med_cols = [c for c in med_df.columns if c.startswith("Medication_")]
    for _, row in med_df.iterrows():
        dis = get_or_create(str(row["Disease"]))
        for col in med_cols:
            val = _clean(row.get(col))
            if val:
                db.add(Medication(disease_id=dis.id, name=val))

    # --- Workouts ---
    wrk_cols = [c for c in wrk_df.columns if c.startswith("workout_")]
    for _, row in wrk_df.iterrows():
        dis = get_or_create(str(row["disease"]))
        for col in wrk_cols:
            val = _clean(row.get(col))
            if val:
                db.add(Workout(disease_id=dis.id, activity=val))

    # --- Diets ---
    diet_cols = [c for c in diet_df.columns if c.startswith("Diet_")]
    for _, row in diet_df.iterrows():
        dis = get_or_create(str(row["Disease"]))
        for col in diet_cols:
            val = _clean(row.get(col))
            if val:
                db.add(Diet(disease_id=dis.id, item=val))

    db.commit()
    print(f"[Seed] Done — {len(disease_map)} diseases seeded.")


def get_recommendations(disease_name: str, db: Session) -> dict:
    """Fetch recommendations for a predicted disease name."""
    # Try exact match first, then case-insensitive
    dis = db.query(Disease).filter(Disease.name == disease_name).first()
    if not dis:
        dis = (
            db.query(Disease)
            .filter(Disease.name.ilike(f"%{disease_name.strip()}%"))
            .first()
        )

    if not dis:
        return {
            "precautions": [],
            "medications": [],
            "workout": [],
            "diet": [],
        }

    return {
        "precautions": [p.text for p in dis.precautions],
        "medications": [m.name for m in dis.medications],
        "workout":     [w.activity for w in dis.workouts],
        "diet":        [d.item for d in dis.diets],
    }
