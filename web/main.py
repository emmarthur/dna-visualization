"""
FastAPI web app for the DNA scrolling animation.

Request flow for someone reading the code:
  GET /           → HTML page (templates/index.html) + static CSS/JS
  GET /stream     → long-lived Server-Sent Events (SSE) connection
  Browser app.js  → EventSource("/stream") receives JSON { "line": "..." } per row

Run locally:
  uvicorn main:app --reload --port 3005
"""

from __future__ import annotations

import json
import sys
import time
from pathlib import Path

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

# dna_core.py lives one directory above web/ (demo root). Add it to import path.
_DEMO_ROOT = Path(__file__).resolve().parent.parent
if str(_DEMO_ROOT) not in sys.path:
    sys.path.insert(0, str(_DEMO_ROOT))

from dna_core import PAUSE, DnaAnimationState, next_row  # noqa: E402

app = FastAPI(title="DNA Visualization")

# Jinja renders index.html; {{ pause_seconds }} is shown in the Help section.
templates = Jinja2Templates(directory=str(Path(__file__).parent / "templates"))

# style.css and app.js — no build step, served as plain static files.
app.mount("/static", StaticFiles(directory=str(Path(__file__).parent / "static")), name="static")


@app.get("/", response_class=HTMLResponse)
async def index(request: Request) -> HTMLResponse:
    """Main page: controls + empty <pre> filled by JavaScript when user clicks Run."""
    return templates.TemplateResponse(
        request,
        "index.html",
        {"pause_seconds": PAUSE},
    )


@app.get("/stream")
async def stream_animation() -> StreamingResponse:
    """
    Stream one helix row at a time to the browser using Server-Sent Events (SSE).

    Each event body is JSON: {"line": "     #A-T#"}.
    The client (static/app.js) parses event.data and appends to the <pre>.

    One SSE connection = one independent animation state (row_index starts at 0).
    Closing the connection (Pause) stops the generator when the client disconnects.
    """

    def events():
        # Sync generator (same pattern as birthday-paradox SSE) so rows stream
        # immediately instead of blocking the async event loop on spacer rows.
        state = DnaAnimationState()
        while True:
            line, state, should_pause = next_row(state)
            payload = json.dumps({"line": line})
            yield f"data: {payload}\n\n"
            if should_pause:
                time.sleep(PAUSE)

    return StreamingResponse(
        events(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )
