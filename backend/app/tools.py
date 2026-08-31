from typing import Dict, Any, List

from .database import (
    get_incidents,
    save_incident,
    add_event,
)


def find_similar_incidents(
    location: str,
    category: str
) -> List[Dict[str, Any]]:

    incidents = get_incidents()

    results = []

    location_words = set(
        location.lower().split()
    )

    for incident in incidents:

        if (
            incident.get("category")
            != category
        ):
            continue

        previous_location = set(
            incident.get(
                "location",
                ""
            ).lower().split()
        )

        overlap = (
            location_words
            & previous_location
        )

        if overlap:

            results.append(
                incident
            )

    return results[:10]


def determine_department(
    category: str
) -> str:

    mapping = {

        "water": "Water & Infrastructure",

        "road": "Roads & Transport",

        "streetlight":
            "Electrical Maintenance",

        "garbage":
            "Sanitation",

        "traffic":
            "Traffic Management",

        "safety":
            "Public Safety",

        "electricity":
            "Electrical Maintenance",

        "other":
            "General Operations",
    }

    return mapping.get(
        category.lower(),
        "General Operations"
    )


def calculate_priority(
    severity: str,
    duplicate_count: int
) -> str:

    if severity == "CRITICAL":
        return "P0"

    if severity == "HIGH":
        return "P1"

    if duplicate_count >= 3:
        return "P1"

    if severity == "MEDIUM":
        return "P2"

    return "P3"


def create_action_plan(
    severity: str,
    department: str,
    priority: str
) -> List[str]:

    plan = [
        f"Route incident to {department}",
        "Create operational task",
        "Monitor response",
    ]

    if priority in ["P0", "P1"]:

        plan.insert(
            1,
            "Request immediate field response"
        )

    if severity in [
        "HIGH",
        "CRITICAL"
    ]:

        plan.append(
            "Escalate automatically if unresolved"
        )

    plan.append(
        "Verify resolution before closure"
    )

    return plan


def simulate_authority_response(
    incident_id: str
):

    incident = get_incident_safe(
        incident_id
    )

    if not incident:
        return None

    add_event(
        incident_id,
        "AUTHORITY_RESPONSE",
        "Maintenance team acknowledged the incident."
    )

    incident[
        "status"
    ] = "IN_PROGRESS"

    incident[
        "assigned_to"
    ] = "Field Response Team"

    save_incident(
        incident
    )

    return incident


def verify_resolution(
    incident_id: str
):

    incident = get_incident_safe(
        incident_id
    )

    if not incident:
        return None

    confidence = 0.87

    incident[
        "resolution_confidence"
    ] = confidence

    if confidence >= 0.80:

        incident[
            "status"
        ] = "RESOLVED"

        add_event(
            incident_id,
            "VERIFICATION",
            "Resolution verified with 87% confidence."
        )

    else:

        incident[
            "status"
        ] = "ESCALATED"

        add_event(
            incident_id,
            "ESCALATION",
            "Resolution confidence was below threshold."
        )

    save_incident(
        incident
    )

    return incident


def get_incident_safe(
    incident_id: str
):

    from .database import get_incident

    return get_incident(
        incident_id
    )