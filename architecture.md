# ACTUATION Architecture

## Overview

ACTUATION is an autonomous incident operations platform.

It transforms an incoming real-world incident into an autonomous operational workflow.

## Flow

Incident
↓
React Dashboard
↓
FastAPI
↓
Google ADK Agent
↓
Gemini
↓
Classification
↓
Duplicate Detection
↓
Priority Decision
↓
Department Routing
↓
Action Plan
↓
Pub/Sub
↓
Background Processing
↓
Firestore
↓
Resolution Verification
↓
Resolve / Escalate

## Components

### Frontend

React + Vite

Provides:

- Incident submission
- Live incident stream
- Agent activity timeline
- Resolution state
- Priority and severity
- Action plan

### Backend

FastAPI

Provides:

- Incident APIs
- Agent workflow
- Event stream
- Firestore integration
- Pub/Sub integration

### Agent

Google ADK + Gemini

The agent is responsible for autonomous reasoning and tool-driven decisions.

### Database

Cloud Firestore

Stores:

- Incidents
- Historical incidents
- Agent events
- Resolution state

### Event infrastructure

Google Cloud Pub/Sub

Used for asynchronous incident processing.

### Deployment

Google Cloud Run

Runs the backend as a serverless container.

## Autonomous Loop

ACTUATION follows:

DETECT
→ DECIDE
→ ACT
→ MONITOR
→ VERIFY
→ RESOLVE

If resolution confidence is insufficient:

VERIFY
→ ESCALATE
