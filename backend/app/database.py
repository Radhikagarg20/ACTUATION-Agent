from datetime import datetime, timezone
from typing import Dict, Any, List

from .config import USE_FIRESTORE

_memory_incidents: Dict[str, Dict[str, Any]] = {}
_memory_events: Dict[str, List[Dict[str, Any]]] = {}

_firestore = None


def init_firestore():

    global _firestore

    if not USE_FIRESTORE:
        return None

    try:
        from google.cloud import firestore

        _firestore = firestore.Client()

        return _firestore

    except Exception as exc:

        print(
            f"[Firestore] Falling back to memory: {exc}"
        )

        _firestore = None

        return None


def save_incident(data: Dict[str, Any]):

    if _firestore:

        _firestore.collection(
            "incidents"
        ).document(data["id"]).set(
            data,
            merge=True
        )

    _memory_incidents[data["id"]] = data

    return data


def get_incident(incident_id: str):

    if _firestore:

        doc = (
            _firestore
            .collection("incidents")
            .document(incident_id)
            .get()
        )

        if doc.exists:
            return doc.to_dict()

    return _memory_incidents.get(incident_id)


def get_incidents():

    if _firestore:

        docs = (
            _firestore
            .collection("incidents")
            .stream()
        )

        return [
            doc.to_dict()
            for doc in docs
        ]

    return list(
        _memory_incidents.values()
    )


def add_event(
    incident_id: str,
    event_type: str,
    message: str
):

    event = {
        "incident_id": incident_id,
        "type": event_type,
        "message": message,
        "timestamp": datetime.now(
            timezone.utc
        ).isoformat(),
        "agent": "ACTUATION",
    }

    if incident_id not in _memory_events:

        _memory_events[incident_id] = []

    _memory_events[
        incident_id
    ].append(event)

    if _firestore:

        (
            _firestore
            .collection("incidents")
            .document(incident_id)
            .collection("events")
            .add(event)
        )

    print(
        f"[ACTUATION] {event_type}: {message}"
    )

    return event


def get_events(incident_id: str):

    if _firestore:

        docs = (
            _firestore
            .collection("incidents")
            .document(incident_id)
            .collection("events")
            .order_by("timestamp")
            .stream()
        )

        return [
            doc.to_dict()
            for doc in docs
        ]

    return _memory_events.get(
        incident_id,
        []
    )