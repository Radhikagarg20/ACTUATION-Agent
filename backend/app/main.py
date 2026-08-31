import asyncio

from fastapi import (
    FastAPI,
    HTTPException,
    BackgroundTasks,
)
from fastapi.middleware.cors import CORSMiddleware

from .config import (
    APP_NAME,
    APP_VERSION,
)

from .database import (
    init_firestore,
    get_incident,
    get_incidents,
    get_events,
)

from .models import IncidentCreate

from .workflow import (
    create_and_process_incident
)


app = FastAPI(
    title=APP_NAME,
    version=APP_VERSION,
    description=(
        "ACTUATION - Autonomous Incident Operations"
    )
)


app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.on_event("startup")
def startup():

    init_firestore()


@app.get("/")
def root():

    return {
        "name": APP_NAME,
        "version": APP_VERSION,
        "status": "operational",
        "mission": (
            "Detect. Decide. Act. Verify. Resolve."
        )
    }


@app.get("/health")
def health():

    return {
        "status": "healthy"
    }


@app.post("/api/incidents")
async def create_incident(
    payload: IncidentCreate,
    background_tasks: BackgroundTasks
):

    if not payload.title.strip():

        raise HTTPException(
            status_code=400,
            detail="Title is required."
        )

    if not payload.description.strip():

        raise HTTPException(
            status_code=400,
            detail="Description is required."
        )

    # Run the workflow asynchronously
    background_tasks.add_task(
        create_and_process_incident,
        payload
    )

    return {
        "status": "accepted",
        "message": (
            "ACTUATION agent started "
            "processing the incident."
        )
    }


@app.post("/api/incidents/sync")
async def create_incident_sync(
    payload: IncidentCreate
):

    result = (
        create_and_process_incident(
            payload
        )
    )

    return result


@app.get("/api/incidents")
def list_incidents():

    return {
        "incidents": get_incidents()
    }


@app.get("/api/incidents/{incident_id}")
def incident(
    incident_id: str
):

    result = get_incident(
        incident_id
    )

    if not result:

        raise HTTPException(
            status_code=404,
            detail="Incident not found."
        )

    return result


@app.get(
    "/api/incidents/{incident_id}/events"
)
def incident_events(
    incident_id: str
):

    return {
        "events":
            get_events(
                incident_id
            )
    }