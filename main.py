#!/usr/bin/env python3
"""
Teranga — AI Marketing Agency
==============================
"Teranga" is the Wolof word for hospitality and generosity —
the spirit with which this agency serves every client.

7 agents, each with a Senegalese name and identity:
  Cheikh Diagne    — Campaign Orchestrator
  Ibrahima Sow     — Marketing Strategist
  Aminata Diallo   — Content Creator
  Rokhaya Ndiaye   — Visual Prompt Designer
  Samba Mbaye      — Video Scriptwriter
  Ousmane Faye     — Marketing Analyst
  Fatou Sarr       — Presentation Agent

Outputs per run:
  - Marketing strategy
  - Social media posts (4 platforms)
  - Email sequence (5 emails)
  - Ad copy (3 platforms)
  - Image generation prompts (6 assets)
  - Video scripts (60s + 15s)
  - KPI tracking plan
  - Client report (Markdown + JSON)

Usage:
    source ~/crewai-env/bin/activate
    cd ~/teranga
    python main.py

Supabase integration:
    Load outputs/<run>/campaign_output.json and insert into your
    Supabase campaigns table. Field names are snake_case and ready.
"""
import os
from dotenv import load_dotenv

load_dotenv()

from src.crew import build_crew, save_outputs


# ──────────────────────────────────────────────────────────────────
# DEMO BRIEF — replace with real client data or use interactive mode
# ──────────────────────────────────────────────────────────────────
DEFAULT_BRIEF = {
    "client_name": "EcoWear",
    "industry": "Sustainable Fashion",
    "product_service": "Eco-friendly activewear made from recycled ocean plastic",
    "target_audience": (
        "Health-conscious millennials and Gen Z (ages 22-38), urban professionals "
        "who prioritize sustainability, fitness, and ethical consumption"
    ),
    "campaign_objective": (
        "Launch the Spring 2025 collection, drive 500 pre-orders in 30 days, "
        "and grow Instagram following from 4K to 10K"
    ),
    "budget": "$15,000 USD total",
    "timeline": "6 weeks — April 1 to May 15, 2025",
    "unique_selling_proposition": (
        "Every product removes 5 plastic bottles from the ocean and ships carbon-neutral. "
        "Performance-grade activewear that's better for you and the planet."
    ),
    "competitors": "Patagonia, Allbirds, Girlfriend Collective, Vuori",
    "tone_of_voice": (
        "Inspiring, authentic, and bold — not preachy or guilt-driven. "
        "Empowering and action-oriented. Speaks to doers, not just dreamers."
    ),
    "additional_notes": (
        "Brand colors: ocean blue (#1B6CA8) and forest green (#2D6A4F). "
        "Founder story: ex-marine biologist turned entrepreneur. "
        "Key visual motif: ocean meets mountain."
    ),
}

TEAM = [
    ("Cheikh Diagne",  "Campaign Orchestrator"),
    ("Ibrahima Sow",   "Marketing Strategist"),
    ("Aminata Diallo", "Content Creator"),
    ("Rokhaya Ndiaye", "Visual Prompt Designer"),
    ("Samba Mbaye",    "Video Scriptwriter"),
    ("Ousmane Faye",   "Marketing Analyst"),
    ("Fatou Sarr",     "Presentation Agent"),
]


def prompt_brief() -> dict:
    fields = [
        ("client_name",                "Client / Brand Name",         True),
        ("industry",                   "Industry",                    True),
        ("product_service",            "Product or Service",          True),
        ("target_audience",            "Target Audience",             True),
        ("campaign_objective",         "Campaign Objective",          True),
        ("budget",                     "Budget (e.g. $20,000)",       False),
        ("timeline",                   "Timeline (e.g. 8 weeks)",     False),
        ("unique_selling_proposition", "Unique Selling Proposition",  True),
        ("competitors",                "Main Competitors",            False),
        ("tone_of_voice",              "Tone of Voice",               False),
        ("additional_notes",           "Additional Notes",            False),
    ]
    print("\nFill in the client brief (* = required):\n")
    brief = {}
    for key, label, required in fields:
        marker = "*" if required else " "
        val = input(f"  [{marker}] {label}: ").strip()
        if required and not val:
            val = f"[{label} not provided]"
        if val:
            brief[key] = val
    return brief


def print_banner(client: str) -> None:
    w = 66
    print("\n" + "═" * w)
    print("  TERANGA — AI Marketing Agency".center(w))
    print("  «L'hospitalité au service de votre marque»".center(w))
    print("═" * w)
    print(f"  Client : {client}")
    print(f"  Team   :")
    for name, role in TEAM:
        print(f"           · {name:<18} {role}")
    print("═" * w + "\n")


def main() -> None:
    w = 66
    print("\n" + "═" * w)
    print("  TERANGA — AI Marketing Agency".center(w))
    print("═" * w)
    print("\n  1. Run with demo brief  (EcoWear — Sustainable Fashion)")
    print("  2. Enter your own client brief")
    print()

    choice = input("  Choice [1/2]: ").strip()
    brief = prompt_brief() if choice == "2" else DEFAULT_BRIEF
    client = brief.get("client_name", "Client")

    print_banner(client)

    crew = build_crew(brief)
    result = crew.kickoff()

    md_path, json_path = save_outputs(result, brief)

    print("\n" + "═" * w)
    print("  Campaign complete!".center(w))
    print("═" * w)
    print(f"  Markdown : {md_path}")
    print(f"  JSON     : {json_path}")
    print("═" * w)
    print()
    print("  Next: insert campaign_output.json into your Supabase campaigns table.")
    print()


if __name__ == "__main__":
    main()
