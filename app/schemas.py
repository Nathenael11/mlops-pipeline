"""
Pydantic Schemas for Machine Telemetry Input and Prediction API Contract
Author: Nathenael Ermias
"""

from typing import Literal
from datetime import datetime
from pydantic import BaseModel, Field, model_validator

class MachineTelemetryInput(BaseModel):
    air_temperature: float = Field(
        ...,
        ge=280.0,
        le=320.0,
        description="Air temperature in Kelvin [K]",
        json_schema_extra={"example": 300.0}
    )
    process_temperature: float = Field(
        ...,
        ge=290.0,
        le=330.0,
        description="Process temperature in Kelvin [K]",
        json_schema_extra={"example": 310.0}
    )
    rotational_speed: float = Field(
        ...,
        ge=1000.0,
        le=3000.0,
        description="Rotational speed in revolutions per minute [RPM]",
        json_schema_extra={"example": 1500.0}
    )
    torque: float = Field(
        ...,
        ge=0.0,
        le=100.0,
        description="Torque force in Newton-meters [Nm]",
        json_schema_extra={"example": 40.0}
    )
    tool_wear: float = Field(
        ...,
        ge=0.0,
        le=300.0,
        description="Tool wear time in minutes [min]",
        json_schema_extra={"example": 45.0}
    )
    product_type: Literal['L', 'M', 'H', 'l', 'm', 'h'] = Field(
        ...,
        description="Product quality grade variant: L (Low - 50%), M (Medium - 30%), H (High - 20%)",
        json_schema_extra={"example": "L"}
    )

    @model_validator(mode='after')
    def validate_temperature_relationship(self) -> 'MachineTelemetryInput':
        if self.process_temperature <= self.air_temperature:
            raise ValueError(
                f"Process temperature ({self.process_temperature} K) must be strictly greater "
                f"than air temperature ({self.air_temperature} K)."
            )
        return self

    model_config = {
        "json_schema_extra": {
            "example": {
                "air_temperature": 300.0,
                "process_temperature": 310.0,
                "rotational_speed": 1500.0,
                "torque": 40.0,
                "tool_wear": 45.0,
                "product_type": "L"
            }
        }
    }

class PredictionResponse(BaseModel):
    risk_score: float = Field(..., description="Estimated probability of machine failure (0.0 to 100.0%)", json_schema_extra={"example": 12.4})
    prediction: str = Field(..., description="Binary classification prediction: 'Failure' or 'No Failure'", json_schema_extra={"example": "No Failure"})
    is_failure: bool = Field(..., description="Boolean flag indicating failure risk", json_schema_extra={"example": False})
    confidence: float = Field(..., description="Model classification confidence percentage", json_schema_extra={"example": 91.8})
    threshold_used: float = Field(..., description="False Discovery Rate (FDR) optimal decision threshold", json_schema_extra={"example": 0.76})
    recommended_action: str = Field(..., description="Prescriptive maintenance action recommendation")
    timestamp: str = Field(..., description="ISO 8601 prediction timestamp")

class HealthResponse(BaseModel):
    status: str = Field(..., json_schema_extra={"example": "healthy"})
    model_loaded: bool = Field(..., json_schema_extra={"example": True})
    optimal_threshold: float = Field(..., json_schema_extra={"example": 0.76})
    version: str = Field(..., json_schema_extra={"example": "1.0.0"})
    author: str = Field(..., json_schema_extra={"example": "Nathenael Ermias"})
