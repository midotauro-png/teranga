"""
Background campaign runner.
Uses a ThreadPoolExecutor so crewAI's blocking kickoff() never touches
the uvicorn event loop — polling requests stay fast.
"""
import uuid
import traceback
import threading
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from pathlib import Path

from src.crew import build_crew, save_outputs

# One shared executor — max 3 parallel campaigns
_executor = ThreadPoolExecutor(max_workers=3, thread_name_prefix="teranga-crew")

# In-memory job store  {campaign_id: dict}
_jobs: dict[str, dict] = {}
_lock = threading.Lock()


def get_job(campaign_id: str) -> dict | None:
    with _lock:
        return _jobs.get(campaign_id)


def list_jobs() -> list[dict]:
    with _lock:
        return list(_jobs.values())


def register(brief: dict) -> str:
    """Create a job record and return its campaign_id."""
    campaign_id = str(uuid.uuid4())
    with _lock:
        _jobs[campaign_id] = {
            "campaign_id": campaign_id,
            "client_name": brief.get("client_name", "Unknown"),
            "status":      "running",
            "started_at":  datetime.now(timezone.utc).isoformat(),
            "finished_at": None,
            "output_dir":  None,
            "error":       None,
        }
    return campaign_id


def _run(campaign_id: str, brief: dict) -> None:
    """Blocking worker — runs inside the ThreadPoolExecutor."""
    try:
        crew   = build_crew(brief)
        result = crew.kickoff()
        md_path, _ = save_outputs(result, brief)

        with _lock:
            _jobs[campaign_id].update({
                "status":      "done",
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "output_dir":  str(Path(md_path).parent),
            })

    except Exception:
        with _lock:
            _jobs[campaign_id].update({
                "status":      "error",
                "finished_at": datetime.now(timezone.utc).isoformat(),
                "error":       traceback.format_exc(),
            })
