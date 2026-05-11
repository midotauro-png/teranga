import json
import re
import uuid
from datetime import datetime
from pathlib import Path

from crewai import Crew, Process, CrewOutput

from .agents import create_agents
from .tasks import create_tasks, create_solo_tasks


def build_crew(brief: dict) -> Crew:
    agents = create_agents()
    selected = brief.get("selected_agents") or []

    if selected:
        tasks = create_solo_tasks(agents, brief, selected)
        # Only include agents that are actually used
        used = {t.agent for t in tasks}
        agent_list = [a for a in agents.values() if a in used]
    else:
        tasks = create_tasks(agents, brief)
        agent_list = list(agents.values())

    return Crew(
        agents=agent_list,
        tasks=tasks,
        process=Process.sequential,
        verbose=True,
        # ── Rate-limit safety net ──
        # Anthropic's per-minute input-token cap (30k on some plans) can be tripped
        # by the presenter task which concatenates all prior outputs. Pacing at
        # 3 requests/minute spreads tokens across a wider window.
        max_rpm=3,
    )


def extract_json(text: str) -> dict | None:
    """Try multiple strategies to extract a JSON object from text."""
    # Strategy 1: ```json code block
    for raw in reversed(re.findall(r"```json\s*([\s\S]*?)\s*```", text)):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            continue

    # Strategy 2: ``` code block without language tag
    for raw in reversed(re.findall(r"```\s*(\{[\s\S]*?\})\s*```", text)):
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            continue

    # Strategy 3: outermost bare { ... }
    start = text.find("{")
    if start != -1:
        depth, i = 0, start
        while i < len(text):
            if text[i] == "{":
                depth += 1
            elif text[i] == "}":
                depth -= 1
                if depth == 0:
                    try:
                        return json.loads(text[start : i + 1])
                    except json.JSONDecodeError:
                        break
            i += 1

    return None


def _is_campaign_json(data: dict) -> bool:
    keys = {"social_posts", "email_sequence", "kpis", "strategy", "ad_copies"}
    return bool(keys & set(data.keys()))


def ensure_meta(data: dict, brief: dict) -> dict:
    data.setdefault("campaign_id", str(uuid.uuid4()))
    data.setdefault("created_at", datetime.now().isoformat())
    data.setdefault("client_name", brief.get("client_name", "Unknown"))
    return data


def save_outputs(result: CrewOutput | str, brief: dict) -> tuple[Path, Path]:
    client = brief.get("client_name", "client").replace(" ", "_").lower()
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    output_dir = Path("outputs") / f"{timestamp}_{client}"
    output_dir.mkdir(parents=True, exist_ok=True)

    # ── Pull individual task outputs ───────────────────────────────
    task_texts: list[str] = []
    if isinstance(result, CrewOutput) and hasattr(result, "tasks_output"):
        task_texts = [
            getattr(t, "raw", None) or str(t)
            for t in (result.tasks_output or [])
        ]

    # Task 6 (index 5) = Fatou's Markdown report
    # Task 7 (index 6) = Cheikh's JSON payload
    markdown_text = task_texts[5] if len(task_texts) > 5 else str(result)
    json_source   = task_texts[6] if len(task_texts) > 6 else str(result)

    # ── Write Markdown ─────────────────────────────────────────────
    md_path = output_dir / "campaign_output.md"
    md_path.write_text(markdown_text, encoding="utf-8")

    # ── Extract JSON — try Cheikh's output first, then all others ──
    json_data = extract_json(json_source)
    if not json_data or not _is_campaign_json(json_data):
        for text in reversed(task_texts):
            json_data = extract_json(text)
            if json_data and _is_campaign_json(json_data):
                break
            json_data = None

    # ── Write JSON ─────────────────────────────────────────────────
    json_path = output_dir / "campaign_output.json"
    if json_data:
        json_data = ensure_meta(json_data, brief)
        json_path.write_text(
            json.dumps(json_data, indent=2, ensure_ascii=False), encoding="utf-8"
        )
    else:
        # Preserve all raw task outputs so nothing is lost
        fallback = {
            "campaign_id": str(uuid.uuid4()),
            "created_at": datetime.now().isoformat(),
            "client_name": brief.get("client_name", "Unknown"),
            "warning": "Structured JSON not found — raw task outputs preserved",
            "task_outputs": task_texts,
        }
        json_path.write_text(
            json.dumps(fallback, indent=2, ensure_ascii=False), encoding="utf-8"
        )

    return md_path, json_path
