import uuid
from datetime import datetime, timezone

from .agent import analyze_incident

from .database import (
    save_incident,
    add_event,
    get_incident,
)

from .tools import (
    find_similar_incidents,
    determine_department,
    calculate_priority,
    create_action_plan,
    simulate_authority_response,
    verify_resolution,
)


def now():
    return datetime.now(
        timezone.utc
    ).isoformat()


def generate_id():

    return (
        "ACT-"
        + uuid.uuid4()
        .hex[:8]
        .upper()
    )


def create_and_process_incident(
    payload
):

    incident_id = generate_id()

    incident = {

        "id": incident_id,

        "title":
            payload.title,

        "description":
            payload.description,

        "location":
            payload.location,

        "category":
            payload.category,

        "reporter":
            payload.reporter,

        "image_url":
            payload.image_url,

        "severity":
            "ANALYZING",

        "priority":
            "ANALYZING",

        "department":
            "ANALYZING",

        "status":
            "RECEIVED",

        "confidence":
            0.0,

        "duplicate_count":
            0,

        "action_plan":
            [],

        "assigned_to":
            None,

        "resolution_confidence":
            0.0,

        "created_at":
            now(),

        "updated_at":
            now(),
    }

    save_incident(
        incident
    )

    add_event(
        incident_id,
        "RECEIVED",
        "Incident received by ACTUATION."
    )

    # -------------------------------------------------
    # AI ANALYSIS
    # -------------------------------------------------

    add_event(
        incident_id,
        "AI_ANALYSIS",
        "Gemini is analyzing the incident."
    )

    analysis = analyze_incident(
        payload.title,
        payload.description,
        payload.location
    )

    category = (
        payload.category
        or analysis.get(
            "category",
            "other"
        )
    )

    severity = analysis.get(
        "severity",
        "MEDIUM"
    )

    confidence = float(
        analysis.get(
            "confidence",
            0.75
        )
    )

    add_event(
        incident_id,
        "CLASSIFIED",
        f"Incident classified as {category}."
    )

    # -------------------------------------------------
    # DUPLICATE DETECTION
    # -------------------------------------------------

    similar = find_similar_incidents(
        payload.location,
        category
    )

    duplicate_count = len(
        [
            item for item in similar
            if item["id"] != incident_id
        ]
    )

    if duplicate_count:

        add_event(
            incident_id,
            "DUPLICATES",
            f"{duplicate_count} similar historical incidents found."
        )

    else:

        add_event(
            incident_id,
            "DUPLICATES",
            "No matching historical incidents found."
        )

    # -------------------------------------------------
    # DEPARTMENT
    # -------------------------------------------------

    department = determine_department(
        category
    )

    add_event(
        incident_id,
        "ROUTED",
        f"Responsible department: {department}."
    )

    # -------------------------------------------------
    # PRIORITY
    # -------------------------------------------------

    priority = calculate_priority(
        severity,
        duplicate_count
    )

    add_event(
        incident_id,
        "PRIORITIZED",
        f"Priority assigned: {priority}."
    )

    # -------------------------------------------------
    # ACTION PLAN
    # -------------------------------------------------

    action_plan = create_action_plan(
        severity,
        department,
        priority
    )

    add_event(
        incident_id,
        "ACTION_PLAN",
        "Autonomous response plan created."
    )

    # -------------------------------------------------
    # UPDATE
    # -------------------------------------------------

    incident.update({

        "category":
            category,

        "severity":
            severity,

        "priority":
            priority,

        "department":
            department,

        "confidence":
            confidence,

        "duplicate_count":
            duplicate_count,

        "action_plan":
            action_plan,

        "status":
            "ACTION_REQUIRED",

        "updated_at":
            now(),
    })

    save_incident(
        incident
    )

    # -------------------------------------------------
    # AUTONOMOUS ACTION
    # -------------------------------------------------

    add_event(
        incident_id,
        "AUTONOMOUS_ACTION",
        "ACTUATION initiated operational response."
    )

    simulate_authority_response(
        incident_id
    )

    # -------------------------------------------------
    # VERIFICATION
    # -------------------------------------------------

    add_event(
        incident_id,
        "VERIFICATION",
        "ACTUATION is verifying resolution."
    )

    verify_resolution(
        incident_id
    )

    final = get_incident(
        incident_id
    )

    return final