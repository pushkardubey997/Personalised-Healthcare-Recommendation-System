from pydantic import BaseModel, field_validator
from typing import List


class PredictRequest(BaseModel):
    symptoms: List[int]

    @field_validator("symptoms")
    @classmethod
    def validate_symptoms(cls, v):
        if len(v) != 605:
            raise ValueError(f"symptoms vector must have exactly 605 elements, got {len(v)}")
        if any(x not in (0, 1) for x in v):
            raise ValueError("symptoms vector must contain only binary values (0 or 1)")
        return v


class RecommendationsSchema(BaseModel):
    precautions: List[str]
    medications: List[str]
    workout: List[str]
    diet: List[str]


class PredictResponse(BaseModel):
    disease: str
    recommendations: RecommendationsSchema


class FeaturesResponse(BaseModel):
    features: List[str]
    total: int
