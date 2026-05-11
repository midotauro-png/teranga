"""
Research tools for Teranga agents.

Returns a list of CrewAI-compatible search tools based on which API keys
are available in the environment. If neither SERPER_API_KEY nor TAVILY_API_KEY
is set, returns an empty list so agents fall back to pure reasoning without
crashing.

Priority:
  1. SerperDevTool   — if SERPER_API_KEY is set (Google SERP)
  2. TavilySearchTool — if TAVILY_API_KEY is set (AI-optimized research)

Both can be active simultaneously; the agent chooses per query.
"""
from __future__ import annotations

import os
from typing import List


def get_search_tools() -> List:
    tools: List = []

    # ── Serper (Google SERP) ──────────────────────────────────────
    if os.getenv("SERPER_API_KEY"):
        try:
            from crewai_tools import SerperDevTool
            tools.append(SerperDevTool())
            print("  [tools] SerperDevTool enabled (Google search)")
        except Exception as e:
            print(f"  [tools] SerperDevTool unavailable: {e}")

    # ── Tavily (AI research search) ───────────────────────────────
    if os.getenv("TAVILY_API_KEY"):
        try:
            # crewai-tools exposes Tavily under different names across versions
            TavilyTool = None
            try:
                from crewai_tools import TavilySearchTool as TavilyTool  # newer
            except ImportError:
                try:
                    from crewai_tools import TavilyTool  # older
                except ImportError:
                    from crewai_tools.tools.tavily_search_tool.tavily_search_tool import (
                        TavilySearchTool as TavilyTool,
                    )
            if TavilyTool is not None:
                tools.append(TavilyTool())
                print("  [tools] Tavily search enabled (AI research)")
        except Exception as e:
            print(f"  [tools] Tavily unavailable: {e}")

    if not tools:
        print("  [tools] No search API keys found — agents run on model knowledge only.")
        print("          Set SERPER_API_KEY and/or TAVILY_API_KEY in .env to enable deep research.")

    return tools
