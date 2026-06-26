from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.schemas.prediction import PredictRequest, PredictResponse, RecommendationsSchema
from app.services.model_service import predict, get_features
from app.services.recommendation_service import get_recommendations

router = APIRouter()


@router.post("/predict", response_model=PredictResponse, summary="Predict disease from symptom vector")
def predict_disease(payload: PredictRequest, db: Session = Depends(get_db)):
    feature_list = get_features()
    if len(payload.symptoms) != len(feature_list):
        raise HTTPException(
            status_code=422,
            detail=f"Expected {len(feature_list)} symptoms, got {len(payload.symptoms)}",
        )

    disease_name = predict(payload.symptoms)
    recs = get_recommendations(disease_name, db)

    return PredictResponse(
        disease=disease_name,
        recommendations=RecommendationsSchema(
            precautions=recs["precautions"],
            medications=recs["medications"],
            workout=recs["workout"],
            diet=recs["diet"],
        ),
    )
