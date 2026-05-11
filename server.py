#!/usr/bin/env python3
"""
Teranga API Server
==================
Start:
    source ~/crewai-env/bin/activate
    cd ~/teranga
    python server.py

Endpoints:
    GET  /                              → Web UI
    POST /api/campaigns                 → Submit brief, get campaign_id
    GET  /api/campaigns                 → List all runs (this session)
    GET  /api/campaigns/{id}            → Poll status (running|done|error)
    GET  /api/campaigns/{id}/result     → Full JSON campaign payload
    GET  /api/campaigns/{id}/report     → Markdown report
    GET  /api/outputs                   → All runs saved on disk
    GET  /docs                          → Interactive Swagger UI
"""
import os
from dotenv import load_dotenv

load_dotenv()

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

from api.routes   import router
from api.ui       import ui_router

app = FastAPI(
    title="Teranga — AI Marketing Agency",
    description=(
        "7 Senegalese-named AI agents that transform a client brief into "
        "a full marketing campaign: strategy, social posts, emails, ads, "
        "image prompts, video scripts, KPIs, and a client report."
    ),
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # tighten when connecting to Next.js in prod
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")
app.include_router(ui_router)
app.include_router(router, prefix="/api")


if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    print(f"""
╔══════════════════════════════════════════════════╗
║         TERANGA — AI Marketing Agency            ║
╠══════════════════════════════════════════════════╣
║  Web UI  →  http://localhost:{port}                ║
║  API     →  http://localhost:{port}/api/campaigns  ║
║  Docs    →  http://localhost:{port}/docs            ║
╚══════════════════════════════════════════════════╝
    """)
    uvicorn.run("server:app", host="0.0.0.0", port=port, reload=False)
