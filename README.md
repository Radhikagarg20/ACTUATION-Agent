# ACTUATION

## Autonomous Incident Operations

> Detect. Decide. Act. Verify. Resolve.

ACTUATION is an autonomous AI incident-response platform built with Gemini, Google ADK and Google Cloud.

Instead of simply collecting incident reports, ACTUATION autonomously:

1. Understands the incident
2. Classifies it
3. Detects similar historical incidents
4. Determines severity
5. Assigns priority
6. Routes the incident
7. Creates an action plan
8. Initiates an operational response
9. Monitors the incident
10. Verifies resolution
11. Escalates unresolved incidents

## Technology

- Gemini
- Google ADK
- Python
- FastAPI
- React
- Firestore
- Pub/Sub
- Cloud Run

## Local Setup

### Backend

```bash
cd backend

python -m venv .venv

# Windows
.venv\Scripts\activate

# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt

copy .env.example .env
