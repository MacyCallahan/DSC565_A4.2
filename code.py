"""Baseline Email Assistant, Part 8: the triage step and the main agent

This script builds an email assistant that:
- Classifies incoming messages (respond, ignore, notify)
- Drafts responses
- Schedules meetings

We'll start with a simple implementation - one that uses hard-coded rules to handle emails.
This part sets up and tries out the two components. Part 9 joins them into one email agent.
"""

import os
import warnings
from pathlib import Path
from typing import Literal

from dotenv import load_dotenv
from langchain.chat_models import init_chat_model
from langchain_core.tools import tool
from langgraph.prebuilt import create_react_agent
from pydantic import BaseModel, Field

from prompts import agent_system_prompt, triage_system_prompt, triage_user_prompt

# --- Load API tokens for our 3rd party APIs ---

_ = load_dotenv(Path(__file__).with_name(".env"))

if not os.environ.get("OPENAI_API_KEY"):
    raise SystemExit(
        "OPENAI_API_KEY is not set. Open the .env file next to code.py, "
        "paste your OpenAI key after OPENAI_API_KEY=, save it and run again."
    )

# --- Setup a Profile, Prompt and Example Email ---

profile = {
    "name": "Macy",
    "full_name": "Macy Callahan",
    "user_profile_background": "Data scientist enrolled in DSC 565 - Building Generative AI Applications",
}

prompt_instructions = {
    "triage_rules": {
        "lowest": "Spam and advertisements, such as promotions for paid AI writing tools.",
        "low": "Informational messages that need no action, such generative AI newsletters or optional guest talk announcements.",
        "medium": "Routine class matters with no close deadline, such as a classmate asking about a prompt engineering reading.",
        "high": "Time-sensitive coursework, such as a teammate needing RAG pipeline code before tomorrow's project check-in.",
        "highest": "Urgent items that need immediate action, such as the instructor reporting that an LLM API key is exposed in a public repository.",
    },
    "agent_instructions": "Use these tools when appropriate to help manage Macy's DSC 565 coursework efficiently."
}

email = {
    "from": "Project Teammate <teammate@university.edu>",
    "to": "Macy Callahan <macy@university.edu>",
    "subject": "Need RAG pipeline code before tomorrow",
    "body": "Our DSC 565 project check-in is tomorrow. Could you send the RAG pipeline code this evening so I can test the retrieval component?",
}

# --- Define the first part of the agent - triage. ---

llm = init_chat_model("openai:gpt-4o-mini")


class Router(BaseModel):
    """Analyze the unread email and route it according to its content."""

    reasoning: str = Field(
        description="Step-by-step reasoning behind the classification."
    )
    classification: Literal["lowest", "low", "medium", "high", "highest"] = Field(
        description="The DSC 565 triage category: lowest, low, medium, high, or highest.",
    )


llm_router = llm.with_structured_output(Router)

# uncomment to view
#print(triage_system_prompt)
#print(triage_user_prompt)

system_prompt = triage_system_prompt.format(
    full_name=profile["full_name"],
    name=profile["name"],
    examples=(
        "1. lowest - From: GrowthDesk <offers@example.com>\n"
        "Subject: Save 70% on an AI writing assistant\n"
        "Text: Try our paid AI writing tool for your next DSC 565 prompt engineering assignment. Upgrade today for a discount.\n"
        "Classification: lowest\n\n"
        "2. low - From: DSC 565 Newsletter <newsletter@university.edu>\n"
        "Subject: This week's generative AI reading roundup\n"
        "Text: Here are summaries of recent large language model articles. No assignment or response is required.\n"
        "Classification: low\n\n"
        "3. medium - From: Alex <alex@university.edu>\n"
        "Subject: Question about the prompt engineering reading\n"
        "Text: Could you clarify one example in the prompt engineering reading for our DSC 565 discussion next week?\n"
        "Classification: medium\n\n"
        "4. high - From: Project Teammate <teammate@university.edu>\n"
        "Subject: Need RAG pipeline code before tomorrow\n"
        "Text: Our project check-in is tomorrow. Could you send the RAG pipeline code this evening so I can test the retrieval component?\n"
        "Classification: high\n\n"
        "5. highest - From: Instructor <instructor@university.edu>\n"
        "Subject: URGENT: LLM API key exposed publicly\n"
        "Text: Your DSC 565 LLM API key is exposed in a public repository. Revoke it and rotate it immediately, then confirm the repository is private.\n"
        "Classification: highest"
    ),
    user_profile_background=profile["user_profile_background"],
    triage_lowest=prompt_instructions["triage_rules"]["lowest"],
    triage_low=prompt_instructions["triage_rules"]["low"],
    triage_medium=prompt_instructions["triage_rules"]["medium"],
    triage_high=prompt_instructions["triage_rules"]["high"],
    triage_highest=prompt_instructions["triage_rules"]["highest"],
)

user_prompt = triage_user_prompt.format(
    author=email["from"],
    to=email["to"],
    subject=email["subject"],
    email_thread=email["body"],
)

result = llm_router.invoke(
    [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]
)

print("\n--- Triage result for the example email ---")
print(result)

# --- Main agent, define tools ---


@tool
def write_email(to: str, subject: str, content: str) -> str:
    """Write and send an email."""
    # Placeholder response - in real app would send email
    return f"Email sent to {to} with subject '{subject}'"


@tool
def schedule_meeting(
    attendees: list[str],
    subject: str,
    duration_minutes: int,
    preferred_day: str
) -> str:
    """Schedule a calendar meeting."""
    # Placeholder response - in real app would check calendar and schedule
    return f"Meeting '{subject}' scheduled for {preferred_day} with {len(attendees)} attendees"


@tool
def check_calendar_availability(day: str) -> str:
    """Check calendar availability for a given day."""
    # Placeholder response - in real app would check actual calendar
    return f"Available times on {day}: 9:00 AM, 2:00 PM, 4:00 PM"


# --- Main agent, define prompt ---


def create_prompt(state):
    return [
        {
            "role": "system",
            "content": agent_system_prompt.format(
                instructions=prompt_instructions["agent_instructions"],
                **profile
                )
        }
    ] + state['messages']


print("\n--- agent_system_prompt ---")
print(agent_system_prompt)

tools=[write_email, schedule_meeting, check_calendar_availability]

# LangGraph 1.x marks create_react_agent as deprecated, but it still works and is the
# notebook's call, so it stays. Only this one notice is hidden.
warnings.filterwarnings("ignore", message="create_react_agent has been moved")

agent = create_react_agent(
    "openai:gpt-4o",
    tools=tools,
    prompt=create_prompt,
)

response = agent.invoke(
    {"messages": [{
        "role": "user",
        "content": "what is my availability for tuesday?"
    }]}
)

print("\n--- Main agent: what is my availability for tuesday? ---")
response["messages"][-1].pretty_print()
