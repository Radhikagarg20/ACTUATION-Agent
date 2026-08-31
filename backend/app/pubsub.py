import json

from .config import (
    GOOGLE_CLOUD_PROJECT,
    PUBSUB_TOPIC,
    USE_PUBSUB,
)


def publish_incident(
    incident_id: str
):

    payload = {
        "incident_id": incident_id
    }

    if not USE_PUBSUB:

        return {
            "mode": "local",
            "queued": False
        }

    try:

        from google.cloud import pubsub_v1

        publisher = (
            pubsub_v1.PublisherClient()
        )

        topic_path = publisher.topic_path(
            GOOGLE_CLOUD_PROJECT,
            PUBSUB_TOPIC
        )

        future = publisher.publish(
            topic_path,
            json.dumps(
                payload
            ).encode("utf-8")
        )

        message_id = future.result(
            timeout=30
        )

        return {
            "mode": "pubsub",
            "queued": True,
            "message_id": message_id
        }

    except Exception as exc:

        print(
            f"[PubSub] Error: {exc}"
        )

        return {
            "mode": "fallback",
            "queued": False,
            "error": str(exc)
        }