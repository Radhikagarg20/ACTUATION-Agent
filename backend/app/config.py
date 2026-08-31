import os
from dotenv import load_dotenv

load_dotenv()

APP_NAME = "ACTUATION"
APP_VERSION = "1.0.0"

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")

GOOGLE_CLOUD_PROJECT = os.getenv(
    "GOOGLE_CLOUD_PROJECT",
    ""
)

GOOGLE_CLOUD_LOCATION = os.getenv(
    "GOOGLE_CLOUD_LOCATION",
    "us-central1"
)

PUBSUB_TOPIC = os.getenv(
    "PUBSUB_TOPIC",
    "actuation-incidents"
)

PUBSUB_SUBSCRIPTION = os.getenv(
    "PUBSUB_SUBSCRIPTION",
    "actuation-worker"
)

USE_FIRESTORE = (
    os.getenv("USE_FIRESTORE", "false").lower() == "true"
)

USE_PUBSUB = (
    os.getenv("USE_PUBSUB", "false").lower() == "true"
)

MODEL = os.getenv(
    "MODEL",
    "gemini-3.7-flash"
)