import json
import glob
import asyncio
from pathlib import Path

from fastapi import APIRouter, HTTPException
from fastapi.responses import HTMLResponse

from .models import BriefRequest, CampaignStatus, CampaignSummary
from .runner import register, get_job, list_jobs, _run, _executor

router = APIRouter()


# ── POST /api/campaigns ───────────────────────────────────────────
@router.post("/campaigns", response_model=CampaignStatus, status_code=202)
async def create_campaign(brief: BriefRequest):
    """
    Submit a client brief. Returns campaign_id immediately (202).
    The 7 agents run in the background — poll GET /api/campaigns/{id}.
    """
    brief_dict  = brief.model_dump(exclude_none=True)
    campaign_id = register(brief_dict)

    # Submit to thread pool — never blocks the uvicorn event loop
    loop = asyncio.get_event_loop()
    loop.run_in_executor(_executor, _run, campaign_id, brief_dict)

    return get_job(campaign_id)


# ── GET /api/campaigns ────────────────────────────────────────────
@router.get("/campaigns", response_model=list[CampaignStatus])
async def list_campaigns():
    """All campaign runs since server start."""
    return list_jobs()


# ── GET /api/campaigns/{id} ───────────────────────────────────────
@router.get("/campaigns/{campaign_id}", response_model=CampaignStatus)
async def get_campaign(campaign_id: str):
    """Poll this to check status: running | done | error."""
    job = get_job(campaign_id)
    if not job:
        raise HTTPException(404, f"Campaign {campaign_id!r} not found")
    return job


# ── GET /api/campaigns/{id}/result ───────────────────────────────
@router.get("/campaigns/{campaign_id}/result")
async def get_result(campaign_id: str):
    """Full JSON campaign payload — only available when status = done."""
    job = get_job(campaign_id)
    if not job:
        raise HTTPException(404, f"Campaign {campaign_id!r} not found")
    if job["status"] == "running":
        raise HTTPException(202, "Still running — try again soon")
    if job["status"] == "error":
        raise HTTPException(500, job.get("error", "Unknown error")[:400])

    json_path = Path(job["output_dir"]) / "campaign_output.json"
    if not json_path.exists():
        raise HTTPException(404, "Output file not found")

    return json.loads(json_path.read_text())


# ── GET /api/campaigns/{id}/report ───────────────────────────────
@router.get("/campaigns/{campaign_id}/report", response_class=HTMLResponse)
async def get_report(campaign_id: str):
    """Markdown report rendered as HTML."""
    job = get_job(campaign_id)
    if not job:
        raise HTTPException(404, f"Campaign {campaign_id!r} not found")
    if job["status"] != "done":
        raise HTTPException(202, "Not ready yet")

    md_path = Path(job["output_dir"]) / "campaign_output.md"
    if not md_path.exists():
        raise HTTPException(404, "Report file not found")

    md = md_path.read_text().replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")
    return HTMLResponse(f"""<!DOCTYPE html><html><head>
<meta charset='UTF-8'/>
<style>body{{font-family:'Segoe UI',sans-serif;max-width:860px;margin:2rem auto;
padding:0 1.5rem;line-height:1.7;color:#1a1a2e}}
pre{{background:#1e1e2e;color:#cdd6f4;padding:1.2rem;border-radius:8px;
overflow-x:auto;font-size:.82rem;white-space:pre-wrap}}
h1,h2,h3{{color:#1B6CA8}}h2{{border-bottom:2px solid #e5e7eb;padding-bottom:.4rem}}
table{{border-collapse:collapse;width:100%}}td,th{{border:1px solid #e5e7eb;padding:.5rem .8rem}}
th{{background:#1B6CA8;color:#fff}}</style></head>
<body><pre>{md}</pre></body></html>""")


# ── GET /api/campaigns/{id}/error ────────────────────────────────
@router.get("/campaigns/{campaign_id}/error")
async def get_error(campaign_id: str):
    """Full error traceback for failed runs."""
    job = get_job(campaign_id)
    if not job:
        raise HTTPException(404, f"Campaign {campaign_id!r} not found")
    if job["status"] != "error":
        raise HTTPException(400, f"Campaign status is {job['status']!r}, not 'error'")
    return {"campaign_id": campaign_id, "traceback": job.get("error", "")}


# ── GET /api/outputs ──────────────────────────────────────────────
@router.get("/outputs", response_model=list[CampaignSummary])
async def list_outputs():
    """All campaign runs saved to disk (survives server restarts)."""
    paths = sorted(glob.glob("outputs/*/campaign_output.json"), reverse=True)
    results = []
    for p in paths:
        try:
            data = json.loads(Path(p).read_text())
            if "warning" in data and "raw_output" in data:
                continue   # skip failed extractions
            results.append(CampaignSummary(
                campaign_id=data.get("campaign_id", "—"),
                campaign_name=data.get("campaign_name"),
                client_name=data.get("client_name", "—"),
                created_at=data.get("created_at", "—"),
                output_dir=str(Path(p).parent),
                social_posts=len(data.get("social_posts", [])),
                emails=len(data.get("email_sequence", [])),
                kpis=len(data.get("kpis", [])),
            ))
        except Exception:
            continue
    return results
