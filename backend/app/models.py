from datetime import datetime, timezone
from typing import Optional, List
from pydantic import BaseModel, Field


def utc_now():
    return datetime.now(timezone.utc).isoformat()


class IncidentCreate(BaseModel):
    title: str
    description: str
    location: str
    category: Optional[str] = None
    reporter: Optional[str] = "Anonymous"
    image_url: Optional[str] = None


class Incident(BaseModel):
    id: str
    title: str
    description: str
    location: str

    category: Optional[str] = None
    reporter: str = "Anonymous"
    image_url: Optional[str] = None

    severity: str = "PENDING"
    priority: str = "PENDING"

    department: str = "PENDING"

    status: str = "RECEIVED"

    confidence: float = 0.0

    duplicate_count: int = 0

    action_plan: List[str] = Field(
        default_factory=list
    )

    assigned_to: Optional[str] = None

    resolution_confidence: float = 0.0

    created_at: str = Field(
        default_factory=utc_now
    )

    updated_at: str = Field(
        default_factory=utc_now
    )


class IncidentEvent(BaseModel):
    incident_id: str
    type: str
    message: str
    timestamp: str = Field(
        default_factory=utc_now
    )
    agent: str = "ACTUATION"