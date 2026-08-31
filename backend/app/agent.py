import json
import os

from google.adk.agents import Agent

from .config import MODEL


AGENT_INSTRUCTION = """
You are ACTUATION, an autonomous incident
operations agent.

Your mission is NOT merely to describe incidents.

Your mission is to:

1. Understand incoming incidents.
2. Classify them.
3. Determine severity.
4. Detect recurring or duplicate incidents.
5. Determine the correct operational department.
6. Assign priority.
7. Create a concrete action plan.
8. Update operational state.
9. Monitor progress.
10. Verify resolution.
11. Escalate unresolved incidents.

You operate as an autonomous workflow engine.

Never invent a completed action.

Use tools whenever an action requires
external state.

Available incident categories:

water
road
streetlight
garbage
traffic
safety
electricity
other

Severity levels:

LOW
MEDIUM
HIGH
CRITICAL

Priority:

P0
P1
P2
P3

The goal is:

DETECT → DECIDE → ACT → MONITOR → VERIFY → RESOLVE

When analyzing an incident, return structured JSON
with:

{
    "category": "...",
    "severity": "...",
    "reason": "...",
    "confidence": 0.0,
    "department": "...",
    "priority": "...",
    "action_plan": []
}

Do not expose hidden reasoning.
Provide concise operational explanations.
"""


root_agent = Agent(
    name="actuation_agent",
    model=MODEL,
    instruction=AGENT_INSTRUCTION,
    tools=[]
)


def analyze_incident(
    title: str,
    description: str,
    location: str
):

    prompt = f"""
Analyze this operational incident.

Title:
{title}

Description:
{description}

Location:
{location}

Return ONLY valid JSON:

{{
  "category": "water|road|streetlight|garbage|traffic|safety|electricity|other",
  "severity": "LOW|MEDIUM|HIGH|CRITICAL",
  "reason": "short explanation",
  "confidence": 0.0,
  "department": "responsible department",
  "priority": "P0|P1|P2|P3",
  "action_plan": ["step 1", "step 2"]
}}
"""

    try:

        from google import genai

        client = genai.Client(
            api_key=os.getenv(
                "GEMINI_API_KEY"
            )
        )

        response = client.models.generate_content(
            model=MODEL,
            contents=prompt
        )

        text = response.text.strip()

        if text.startswith("```"):

            text = (
                text
                .replace("```json", "")
                .replace("```", "")
                .strip()
            )

        return json.loads(
            text
        )

    except Exception as exc:

        print(
            f"[Gemini] fallback: {exc}"
        )

        return {
            "category": "other",
            "severity": "MEDIUM",
            "reason": "Operational analysis fallback",
            "confidence": 0.60,
            "department": "General Operations",
            "priority": "P2",
            "action_plan": [
                "Review incident",
                "Assign responsible team",
                "Monitor response",
                "Verify resolution"
            ]
        }