from fastapi import APIRouter
from app.schemas.prediction import FeaturesResponse
from app.services.model_service import get_features

router = APIRouter()


@router.get("/features", response_model=FeaturesResponse, summary="Return ordered symptom feature list")
def list_features():
    features = get_features()
    return FeaturesResponse(features=features, total=len(features))
