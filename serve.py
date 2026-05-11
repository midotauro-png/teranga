#!/usr/bin/env python3
"""
Teranga Viewer — serves the latest campaign as a web page.
Usage:
    source ~/crewai-env/bin/activate
    cd ~/teranga
    python serve.py
Then open: http://localhost:8080
"""
import json
import glob
import webbrowser
import threading
from pathlib import Path
from http.server import HTTPServer, BaseHTTPRequestHandler
from datetime import datetime


def load_latest() -> tuple[dict, str]:
    runs = sorted(glob.glob("outputs/*/campaign_output.json"))
    if not runs:
        return {}, ""
    json_path = runs[-1]
    md_path   = json_path.replace(".json", ".md")
    with open(json_path) as f:
        data = json.load(f)
    md = Path(md_path).read_text() if Path(md_path).exists() else ""
    return data, md


def build_html(data: dict, md: str) -> str:
    cn   = data.get("campaign_name", "Campaign")
    cl   = data.get("client_name",   "Client")
    cid  = data.get("campaign_id",   "—")
    ts   = data.get("created_at",    "—")[:10]
    strat = data.get("strategy", {})

    def cards(items, fields):
        if not items:
            return "<p class='empty'>No data</p>"
        html = ""
        for item in items:
            html += "<div class='card'>"
            for f in fields:
                val = item.get(f, "")
                if isinstance(val, list):
                    val = ", ".join(str(v) for v in val) if val else "—"
                elif isinstance(val, dict):
                    val = json.dumps(val, indent=2)
                html += f"<p><span class='label'>{f.replace('_',' ').title()}</span><span class='val'>{val or '—'}</span></p>"
            html += "</div>"
        return html

    def kpi_table(items):
        if not items:
            return "<p class='empty'>No KPIs</p>"
        rows = ""
        for k in items:
            stage = k.get("funnel_stage", "")
            color = {
                "Awareness": "#1B6CA8", "Engagement": "#2D6A4F",
                "Conversion": "#e07b39", "Retention": "#7b5ea7",
                "Revenue": "#c0392b"
            }.get(stage, "#555")
            rows += f"""<tr>
                <td><span class='badge' style='background:{color}'>{stage}</span></td>
                <td><strong>{k.get('metric','')}</strong></td>
                <td>{k.get('target','')}</td>
                <td>{k.get('baseline','—')}</td>
                <td>{k.get('measurement_method','')}</td>
                <td>{k.get('frequency','')}</td>
            </tr>"""
        return f"""<table><thead><tr>
            <th>Stage</th><th>Metric</th><th>Target</th>
            <th>Baseline</th><th>Method</th><th>Frequency</th>
        </tr></thead><tbody>{rows}</tbody></table>"""

    social_html  = cards(data.get("social_posts",  []), ["platform","caption","hashtags","cta","best_time_to_post"])
    email_html   = cards(data.get("email_sequence", []), ["position","subject","preview_text","body","cta","send_day"])
    ad_html      = cards(data.get("ad_copies",      []), ["platform","headline","description","cta"])
    visual_html  = cards(data.get("image_prompts",  []), ["purpose","style","dimensions","prompt","notes"])
    steps_html   = cards(data.get("next_steps",     []), ["action","owner","due_date"])
    kpi_html     = kpi_table(data.get("kpis", []))

    vid_html = ""
    for v in data.get("video_scripts", []):
        scenes = "".join(
            f"<tr><td>{s.get('scene_number','')}</td><td>{s.get('timecode','')}</td>"
            f"<td>{s.get('visual','')}</td><td>{s.get('voiceover','')}</td>"
            f"<td>{s.get('text_overlay','')}</td></tr>"
            for s in v.get("scenes", [])
        )
        scene_table = f"""<table><thead><tr>
            <th>#</th><th>Time</th><th>Visual</th><th>Voiceover</th><th>Text Overlay</th>
        </tr></thead><tbody>{scenes}</tbody></table>""" if scenes else ""
        vid_html += f"""
        <div class='card'>
            <p><span class='label'>Title</span><span class='val'>{v.get('title','')}</span></p>
            <p><span class='label'>Duration</span><span class='val'>{v.get('duration','')}</span></p>
            <p><span class='label'>Hook</span><span class='val'>{v.get('hook','')}</span></p>
            <p><span class='label'>CTA</span><span class='val'>{v.get('cta','')}</span></p>
            <p><span class='label'>Music</span><span class='val'>{v.get('music_direction','')}</span></p>
            {scene_table}
        </div>"""

    strategy_html = "".join(
        f"<p><span class='label'>{k.replace('_',' ').title()}</span>"
        f"<span class='val'>{json.dumps(v) if isinstance(v,(dict,list)) else v}</span></p>"
        for k, v in strat.items()
    )

    # Markdown section (raw)
    md_escaped = md.replace("&","&amp;").replace("<","&lt;").replace(">","&gt;")

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Teranga — {cl}</title>
<style>
  :root {{
    --blue:  #1B6CA8;
    --green: #2D6A4F;
    --bg:    #f4f6f9;
    --card:  #ffffff;
    --text:  #1a1a2e;
    --muted: #6b7280;
    --border:#e5e7eb;
  }}
  * {{ box-sizing:border-box; margin:0; padding:0; }}
  body {{ font-family:'Segoe UI',system-ui,sans-serif; background:var(--bg); color:var(--text); }}

  /* ── Header ── */
  header {{
    background: linear-gradient(135deg, var(--blue) 0%, var(--green) 100%);
    color:#fff; padding:2.5rem 2rem 2rem;
  }}
  header h1 {{ font-size:1.9rem; font-weight:700; letter-spacing:-.5px; }}
  header p  {{ opacity:.85; margin-top:.4rem; font-size:.95rem; }}
  .meta-chips {{ display:flex; gap:.6rem; flex-wrap:wrap; margin-top:1.2rem; }}
  .chip {{
    background:rgba(255,255,255,.18); border:1px solid rgba(255,255,255,.3);
    border-radius:999px; padding:.25rem .85rem; font-size:.78rem; font-weight:600;
  }}

  /* ── Nav ── */
  nav {{
    background:#fff; border-bottom:1px solid var(--border);
    position:sticky; top:0; z-index:100;
    display:flex; gap:0; overflow-x:auto;
  }}
  nav a {{
    padding:.85rem 1.2rem; font-size:.82rem; font-weight:600; color:var(--muted);
    text-decoration:none; white-space:nowrap; border-bottom:2px solid transparent;
    transition:color .15s, border-color .15s;
  }}
  nav a:hover {{ color:var(--blue); }}
  nav a.active {{ color:var(--blue); border-color:var(--blue); }}

  /* ── Layout ── */
  main {{ max-width:1100px; margin:0 auto; padding:2rem 1.5rem; }}
  section {{ margin-bottom:3rem; scroll-margin-top:4rem; }}
  h2 {{
    font-size:1.25rem; font-weight:700; color:var(--blue);
    border-bottom:2px solid var(--border); padding-bottom:.6rem; margin-bottom:1.2rem;
  }}
  h3 {{ font-size:1rem; font-weight:600; color:var(--green); margin:1.2rem 0 .6rem; }}

  /* ── Cards ── */
  .card-grid {{ display:grid; grid-template-columns:repeat(auto-fill,minmax(320px,1fr)); gap:1rem; }}
  .card {{
    background:var(--card); border:1px solid var(--border);
    border-radius:10px; padding:1.1rem; box-shadow:0 1px 4px rgba(0,0,0,.06);
  }}
  .card p {{ display:flex; flex-direction:column; gap:.15rem; margin-bottom:.7rem; }}
  .card p:last-child {{ margin-bottom:0; }}
  .label {{
    font-size:.7rem; font-weight:700; text-transform:uppercase;
    letter-spacing:.05em; color:var(--muted);
  }}
  .val {{ font-size:.88rem; color:var(--text); line-height:1.5; }}

  /* ── Table ── */
  table {{ width:100%; border-collapse:collapse; font-size:.84rem; background:var(--card); border-radius:8px; overflow:hidden; }}
  th {{ background:var(--blue); color:#fff; padding:.6rem .9rem; text-align:left; font-size:.76rem; text-transform:uppercase; letter-spacing:.04em; }}
  td {{ padding:.65rem .9rem; border-bottom:1px solid var(--border); vertical-align:top; }}
  tr:last-child td {{ border-bottom:none; }}
  tr:nth-child(even) td {{ background:#f9fafb; }}

  /* ── Badge ── */
  .badge {{ border-radius:999px; color:#fff; padding:.2rem .65rem; font-size:.72rem; font-weight:700; display:inline-block; }}

  /* ── Markdown ── */
  .md-box {{
    background:#1e1e2e; color:#cdd6f4; padding:1.5rem;
    border-radius:10px; font-family:'Fira Code','Cascadia Code',monospace;
    font-size:.8rem; line-height:1.7; overflow-x:auto;
    white-space:pre-wrap; max-height:600px; overflow-y:auto;
  }}

  /* ── JSON ── */
  .json-box {{
    background:#1e1e2e; color:#a6e3a1; padding:1.5rem;
    border-radius:10px; font-family:'Fira Code','Cascadia Code',monospace;
    font-size:.78rem; line-height:1.6; overflow:auto;
    max-height:600px; white-space:pre;
  }}

  /* ── Empty ── */
  .empty {{ color:var(--muted); font-style:italic; font-size:.88rem; }}

  /* ── Footer ── */
  footer {{
    text-align:center; padding:2rem; color:var(--muted); font-size:.8rem;
    border-top:1px solid var(--border); margin-top:2rem;
  }}
</style>
</head>
<body>

<header>
  <h1>TERANGA — AI Marketing Agency</h1>
  <p>«L'hospitalité au service de votre marque»</p>
  <div class="meta-chips">
    <span class="chip">Client: {cl}</span>
    <span class="chip">{cn}</span>
    <span class="chip">Generated: {ts}</span>
    <span class="chip">ID: {cid[:8]}…</span>
  </div>
</header>

<nav id="nav">
  <a href="#strategy"  class="active">Strategy</a>
  <a href="#social">Social</a>
  <a href="#email">Emails</a>
  <a href="#ads">Ads</a>
  <a href="#visuals">Visuals</a>
  <a href="#video">Video</a>
  <a href="#kpis">KPIs</a>
  <a href="#nextsteps">Next Steps</a>
  <a href="#report">Full Report</a>
  <a href="#json">JSON</a>
</nav>

<main>

  <section id="strategy">
    <h2>Marketing Strategy</h2>
    <div class="card">{strategy_html}</div>
  </section>

  <section id="social">
    <h2>Social Media Posts</h2>
    <div class="card-grid">{social_html}</div>
  </section>

  <section id="email">
    <h2>Email Sequence</h2>
    <div class="card-grid">{email_html}</div>
  </section>

  <section id="ads">
    <h2>Ad Copy</h2>
    <div class="card-grid">{ad_html}</div>
  </section>

  <section id="visuals">
    <h2>Image Generation Prompts</h2>
    <div class="card-grid">{visual_html}</div>
  </section>

  <section id="video">
    <h2>Video Scripts</h2>
    {vid_html}
  </section>

  <section id="kpis">
    <h2>KPI & Analytics Framework</h2>
    {kpi_html}
  </section>

  <section id="nextsteps">
    <h2>Next Steps</h2>
    <div class="card-grid">{steps_html}</div>
  </section>

  <section id="report">
    <h2>Full Markdown Report</h2>
    <div class="md-box">{md_escaped}</div>
  </section>

  <section id="json">
    <h2>JSON Payload (Supabase-ready)</h2>
    <div class="json-box">{json.dumps(data, indent=2, ensure_ascii=False)}</div>
  </section>

</main>

<footer>
  Teranga AI Marketing Agency &nbsp;·&nbsp;
  Cheikh · Ibrahima · Aminata · Rokhaya · Samba · Ousmane · Fatou
</footer>

<script>
  // Highlight active nav link on scroll
  const sections = document.querySelectorAll('section[id]');
  const links    = document.querySelectorAll('nav a');
  const obs = new IntersectionObserver(entries => {{
    entries.forEach(e => {{
      if (e.isIntersecting) {{
        links.forEach(l => l.classList.remove('active'));
        const a = document.querySelector(`nav a[href="#${{e.target.id}}"]`);
        if (a) a.classList.add('active');
      }}
    }});
  }}, {{ threshold: 0.3 }});
  sections.forEach(s => obs.observe(s));
</script>
</body>
</html>"""


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        data, md = load_latest()
        html = build_html(data, md)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode("utf-8"))

    def log_message(self, fmt, *args):
        pass  # silence default request logs


def main():
    port = 8080
    server = HTTPServer(("localhost", port), Handler)
    url = f"http://localhost:{port}"
    print(f"\n{'═'*50}")
    print(f"  TERANGA Viewer")
    print(f"{'═'*50}")
    print(f"  Open: {url}")
    print(f"  Stop: Ctrl+C")
    print(f"{'═'*50}\n")
    threading.Timer(1, lambda: webbrowser.open(url)).start()
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\n  Server stopped.")


if __name__ == "__main__":
    main()
