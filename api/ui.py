from fastapi import APIRouter
from fastapi.responses import HTMLResponse

ui_router = APIRouter()

HTML = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8"/>
<meta name="viewport" content="width=device-width,initial-scale=1"/>
<title>Teranga — AI Marketing Agency</title>
<link rel="preconnect" href="https://fonts.googleapis.com"/>
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin/>
<link href="https://fonts.googleapis.com/css2?family=Playfair+Display:ital,wght@0,700;1,400;1,700&family=DM+Sans:opsz,wght@9..40,300;9..40,400;9..40,500;9..40,600&display=swap" rel="stylesheet"/>

<style>
/* ── DESIGN TOKENS ─────────────────────────────────────────── */
:root {
  --ebony:      #1A1208;
  --ebony-2:    #221608;
  --ebony-3:    #2C1D0A;
  --ebony-4:    #362410;
  --terra:      #C0472A;
  --terra-d:    #9C3420;
  --ochre:      #C97D20;
  --ochre-d:    #A36318;
  --ochre-l:    #E8A83A;
  --green:      #1E4D2B;
  --green-l:    #2A6B3C;
  --cream:      #F5EDD8;
  --cream-d:    #D4C5A0;
  --cream-dim:  rgba(245,237,216,.55);
  --gold-line:  rgba(201,125,32,.28);
  --gold-glow:  rgba(201,125,32,.12);
  --terra-glow: rgba(192,71,42,.10);
}

/* ── RESET ─────────────────────────────────────────────────── */
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{
  background:var(--ebony);
  color:var(--cream);
  font-family:'DM Sans',sans-serif;
  font-size:16px;
  line-height:1.65;
  overflow-x:hidden;
}

/* ── ADINKRA BACKGROUND SVG WATERMARK ──────────────────────── */
body::before{
  content:'';
  position:fixed;inset:0;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='120' height='120'%3E%3Cg fill='none' stroke='%23C97D20' stroke-width='0.8' opacity='0.04'%3E%3Crect x='20' y='20' width='80' height='80' rx='2'/%3E%3Crect x='35' y='35' width='50' height='50' rx='1'/%3E%3Cline x1='60' y1='20' x2='60' y2='100'/%3E%3Cline x1='20' y1='60' x2='100' y2='60'/%3E%3Ccircle cx='60' cy='60' r='18'/%3E%3Cpolygon points='60,22 70,50 100,50 76,68 84,96 60,78 36,96 44,68 20,50 50,50'/%3E%3C/g%3E%3C/svg%3E");
  background-size:120px 120px;
  pointer-events:none;
  z-index:0;
}

/* ── KENTE BORDER STRIP ────────────────────────────────────── */
.kente{
  height:10px;
  width:100%;
  background:repeating-linear-gradient(
    90deg,
    var(--ochre)    0px,  var(--ochre)    14px,
    var(--ebony)    14px, var(--ebony)    16px,
    var(--terra)    16px, var(--terra)    30px,
    var(--ebony)    30px, var(--ebony)    32px,
    var(--green)    32px, var(--green)    46px,
    var(--ebony)    46px, var(--ebony)    48px,
    var(--cream-d)  48px, var(--cream-d)  54px,
    var(--ebony)    54px, var(--ebony)    56px,
    var(--ochre)    56px, var(--ochre)    70px,
    var(--ebony)    70px, var(--ebony)    72px,
    var(--terra)    72px, var(--terra)    78px,
    var(--ebony)    78px, var(--ebony)    80px
  );
  position:relative;z-index:10;
}
.kente::after{
  content:'';
  display:block;height:3px;
  background:repeating-linear-gradient(
    90deg,
    var(--cream-d) 0px,var(--cream-d) 4px,
    transparent 4px,transparent 12px
  );
}

/* ── NAV ────────────────────────────────────────────────────── */
nav{
  position:sticky;top:0;z-index:100;
  background:rgba(26,18,8,.92);
  backdrop-filter:blur(18px);
  border-bottom:1px solid var(--gold-line);
  padding:.9rem 3rem;
  display:flex;align-items:center;justify-content:space-between;
}
.nav-logo{
  display:flex;align-items:center;gap:.75rem;
  text-decoration:none;
}
.nav-logo-img{
  width:46px;height:46px;
  border-radius:50%;
  object-fit:cover;
  border:1.5px solid rgba(201,125,32,.5);
  box-shadow:0 0 10px rgba(201,125,32,.25),0 0 0 3px rgba(201,125,32,.08);
  background:#000;
  flex-shrink:0;
}
.nav-logo-text{
  font-family:'Playfair Display',serif;
  font-size:1.45rem;font-weight:700;
  color:var(--ochre);
  letter-spacing:.5px;
}
.nav-logo-text span{color:var(--cream);font-style:italic}
.nav-links{display:flex;gap:2rem;list-style:none}
.nav-links a{
  color:var(--cream-dim);font-size:.85rem;font-weight:500;
  text-decoration:none;letter-spacing:.04em;text-transform:uppercase;
  transition:color .2s;
}
.nav-links a:hover{color:var(--ochre)}
.nav-cta{
  background:var(--terra);color:#fff;
  padding:.5rem 1.4rem;border-radius:4px;
  font-size:.82rem;font-weight:600;text-decoration:none;
  letter-spacing:.04em;text-transform:uppercase;
  transition:background .2s;
}
.nav-cta:hover{background:var(--terra-d)}

/* ── SECTION WRAPPER ───────────────────────────────────────── */
.section{
  position:relative;z-index:1;
  max-width:1180px;margin:0 auto;
  padding:5rem 2rem;
}
.section-sm{padding:3rem 2rem}

/* ── DIVIDER ───────────────────────────────────────────────── */
.divider{
  width:100%;height:1px;
  background:linear-gradient(90deg,transparent,var(--gold-line),transparent);
  margin:0;
}

/* ── SECTION LABEL ─────────────────────────────────────────── */
.eyebrow{
  display:inline-flex;align-items:center;gap:.6rem;
  font-size:.72rem;font-weight:600;letter-spacing:.14em;
  text-transform:uppercase;color:var(--ochre);
  margin-bottom:1rem;
}
.eyebrow::before,.eyebrow::after{
  content:'';display:block;
  width:28px;height:1px;background:var(--ochre);opacity:.6;
}

/* ── HEADINGS ──────────────────────────────────────────────── */
h1,h2,h3{font-family:'Playfair Display',serif}
h1{font-size:clamp(2.4rem,5vw,3.8rem);line-height:1.15;font-weight:700}
h2{font-size:clamp(1.8rem,3.5vw,2.6rem);line-height:1.2;font-weight:700}
h3{font-size:1.15rem;font-weight:700}
.italic{font-style:italic}
.gold{color:var(--ochre)}
.terra{color:var(--terra)}
.cream{color:var(--cream)}

/* ════════════════════════════════════════════════════════════
   HERO
═══════════════════════════════════════════════════════════ */
.hero-wrap{
  min-height:92vh;
  display:flex;align-items:center;
  position:relative;overflow:hidden;
  padding:0 2rem;
}
/* Large faded logo watermark */
.hero-wrap .logo-bg{
  position:absolute;
  top:50%;left:50%;
  transform:translate(-50%,-50%);
  width:min(700px,90vw);
  height:min(700px,90vw);
  object-fit:contain;
  opacity:0.055;
  pointer-events:none;
  z-index:0;
  filter:grayscale(20%) blur(1px);
  mix-blend-mode:luminosity;
}
/* warm radial glow behind hero */
.hero-wrap::before{
  content:'';position:absolute;
  top:-10%;left:-5%;
  width:60%;height:110%;
  background:radial-gradient(ellipse at 30% 50%,
    rgba(201,125,32,.08) 0%,
    rgba(192,71,42,.05) 40%,
    transparent 70%);
  pointer-events:none;
}
.hero-wrap::after{
  content:'';position:absolute;
  bottom:-20%;right:0;
  width:50%;height:80%;
  background:radial-gradient(ellipse at 70% 60%,
    rgba(30,77,43,.12) 0%,transparent 65%);
  pointer-events:none;
}
.hero-grid{
  max-width:1180px;width:100%;margin:0 auto;
  display:grid;grid-template-columns:1fr 1fr;
  gap:4rem;align-items:center;
  position:relative;z-index:1;
}
.hero-left{}
.hero-tag{
  display:inline-flex;align-items:center;gap:.5rem;
  background:rgba(201,125,32,.12);
  border:1px solid var(--gold-line);
  border-radius:2px;
  padding:.3rem .9rem;
  font-size:.75rem;font-weight:600;
  letter-spacing:.1em;text-transform:uppercase;color:var(--ochre);
  margin-bottom:1.8rem;
}
.hero-tag svg{width:12px;height:12px;fill:var(--ochre)}
.hero-left h1{margin-bottom:1.4rem}
.hero-left h1 em{
  font-style:italic;color:var(--ochre);
  display:block;
}
.hero-desc{
  color:var(--cream-dim);font-size:1.05rem;
  max-width:480px;margin-bottom:2.2rem;line-height:1.75;
}
.hero-ctas{display:flex;gap:1rem;flex-wrap:wrap;margin-bottom:3rem}
.btn-primary{
  background:var(--terra);color:#fff;
  padding:.85rem 2.2rem;border-radius:4px;
  font-size:.9rem;font-weight:600;
  text-decoration:none;letter-spacing:.04em;
  border:none;cursor:pointer;
  transition:background .2s,transform .15s;
  display:inline-block;
}
.btn-primary:hover{background:var(--terra-d);transform:translateY(-1px)}
.btn-ghost{
  background:transparent;
  color:var(--cream);
  padding:.85rem 2.2rem;border-radius:4px;
  font-size:.9rem;font-weight:500;
  text-decoration:none;letter-spacing:.03em;
  border:1px solid var(--gold-line);cursor:pointer;
  transition:border-color .2s,color .2s;
  display:inline-block;
}
.btn-ghost:hover{border-color:var(--ochre);color:var(--ochre)}
.hero-social-proof{
  display:flex;gap:2rem;
}
.proof-stat{display:flex;flex-direction:column}
.proof-num{
  font-family:'Playfair Display',serif;
  font-size:1.6rem;font-weight:700;color:var(--ochre);
}
.proof-label{font-size:.75rem;color:var(--cream-dim);letter-spacing:.05em}

/* ── Dashboard Card ──────────────────────────────────────── */
.dashboard-card{
  background:var(--ebony-3);
  border:1px solid var(--gold-line);
  border-radius:8px;
  padding:2rem;
  position:relative;
  overflow:hidden;
  box-shadow:0 0 60px rgba(201,125,32,.08),0 20px 60px rgba(0,0,0,.4);
}
.dashboard-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--terra),var(--ochre),var(--green-l));
}
.dash-header{
  display:flex;justify-content:space-between;align-items:center;
  margin-bottom:1.6rem;
}
.dash-title{
  font-family:'Playfair Display',serif;
  font-size:1rem;font-weight:700;color:var(--cream);
}
.dash-live{
  display:flex;align-items:center;gap:.4rem;
  font-size:.72rem;font-weight:600;color:var(--ochre-l);
  letter-spacing:.06em;text-transform:uppercase;
}
.live-dot{
  width:6px;height:6px;border-radius:50%;
  background:var(--ochre-l);
  animation:pulse 1.8s ease-in-out infinite;
}
@keyframes pulse{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.4;transform:scale(.7)}}

.dash-metrics{display:grid;grid-template-columns:1fr 1fr;gap:1rem;margin-bottom:1.6rem}
.metric-box{
  background:var(--ebony-2);border:1px solid var(--gold-line);
  border-radius:6px;padding:1rem;
}
.metric-label{font-size:.7rem;color:var(--cream-dim);letter-spacing:.06em;text-transform:uppercase;margin-bottom:.3rem}
.metric-val{
  font-family:'Playfair Display',serif;
  font-size:1.7rem;font-weight:700;color:var(--ochre);
}
.metric-val.terra{color:var(--terra)!important}
.metric-val.green{color:#4CAF79!important}
.metric-change{font-size:.72rem;color:#4CAF79;margin-top:.2rem}
.metric-change.down{color:var(--terra)}

.dash-bar-label{
  display:flex;justify-content:space-between;
  font-size:.75rem;color:var(--cream-dim);margin-bottom:.4rem;
}
.dash-bar-track{
  background:var(--ebony-2);border-radius:2px;height:6px;
  margin-bottom:.8rem;overflow:hidden;
}
.dash-bar-fill{
  height:100%;border-radius:2px;
  animation:barGrow 2.2s cubic-bezier(.4,0,.2,1) forwards;
  transform-origin:left;
}
@keyframes barGrow{from{width:0}to{width:var(--w)}}

.dash-agents{margin-top:1.4rem;border-top:1px solid var(--gold-line);padding-top:1.2rem}
.dash-agents-title{font-size:.7rem;text-transform:uppercase;letter-spacing:.08em;color:var(--cream-dim);margin-bottom:.7rem}
.agent-row{
  display:flex;align-items:center;gap:.7rem;
  margin-bottom:.5rem;font-size:.78rem;
}
.agent-dot{
  width:7px;height:7px;border-radius:50%;flex-shrink:0;
}
.agent-name{color:var(--cream);font-weight:500}
.agent-status{margin-left:auto;color:var(--ochre-l);font-size:.7rem}
.agent-status.idle{color:var(--cream-dim)}

/* ════════════════════════════════════════════════════════════
   STATS BAR
═══════════════════════════════════════════════════════════ */
.stats-bar{
  background:var(--ebony-3);
  border-top:1px solid var(--gold-line);
  border-bottom:1px solid var(--gold-line);
  padding:1.6rem 2rem;
}
.stats-inner{
  max-width:1180px;margin:0 auto;
  display:flex;justify-content:space-around;align-items:center;
  flex-wrap:wrap;gap:1rem;
}
.stat-item{text-align:center}
.stat-num{
  font-family:'Playfair Display',serif;
  font-size:2rem;font-weight:700;color:var(--ochre);
  display:block;
}
.stat-label{font-size:.72rem;color:var(--cream-dim);letter-spacing:.06em;text-transform:uppercase}
.stat-sep{width:1px;height:40px;background:var(--gold-line)}

/* ════════════════════════════════════════════════════════════
   SERVICES
═══════════════════════════════════════════════════════════ */
.services-grid{
  display:grid;grid-template-columns:repeat(3,1fr);
  gap:1.2rem;margin-top:3rem;
}
.service-card{
  background:var(--ebony-2);
  border:1px solid var(--gold-line);
  border-radius:6px;
  overflow:hidden;
  transition:transform .2s,box-shadow .2s,border-color .2s;
}
.service-card:hover{
  transform:translateY(-4px);
  box-shadow:0 12px 40px rgba(0,0,0,.3);
  border-color:rgba(201,125,32,.5);
}
.service-top{height:3px}
.service-top.ochre{background:linear-gradient(90deg,var(--ochre-d),var(--ochre-l))}
.service-top.terra{background:linear-gradient(90deg,var(--terra-d),var(--terra))}
.service-top.green{background:linear-gradient(90deg,var(--green),var(--green-l))}
.service-body{padding:1.4rem 1.4rem 1.2rem}
/* Agent photo row at top of service card */
.service-agent-row{
  display:flex;align-items:center;gap:.85rem;
  margin-bottom:1.1rem;
}
.service-photo{
  width:64px;height:64px;border-radius:50%;
  border:2px solid var(--gold-line);
  overflow:hidden;flex-shrink:0;
  background:var(--ebony-4);
  transition:border-color .2s;
}
.service-card:hover .service-photo{border-color:var(--ochre)}
.service-photo img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block}
.service-agent-info{}
.service-agent-name{font-size:.8rem;font-weight:600;color:var(--cream);font-family:'Playfair Display',serif}
.service-agent-role{font-size:.68rem;color:var(--ochre);letter-spacing:.05em;text-transform:uppercase}
.service-card h3{font-size:1rem;margin-bottom:.45rem;color:var(--cream)}
.service-card p{font-size:.83rem;color:var(--cream-dim);line-height:1.65}
.service-footer{
  margin-top:1rem;padding-top:.7rem;
  border-top:1px solid rgba(201,125,32,.15);
  display:flex;align-items:center;justify-content:space-between;
}
.service-solo-btn{
  background:transparent;border:1px solid var(--gold-line);
  color:var(--ochre);border-radius:3px;
  padding:.22rem .65rem;font-size:.68rem;font-weight:600;
  letter-spacing:.05em;text-transform:uppercase;cursor:pointer;
  font-family:'DM Sans',sans-serif;
  transition:background .15s,border-color .15s;
}
.service-solo-btn:hover{background:rgba(201,125,32,.12);border-color:var(--ochre)}
/* Featured orchestrator card */
.service-card.featured{
  grid-column:1/-1;
  display:flex;align-items:center;gap:0;
  overflow:hidden;
}
.service-card.featured .service-top{
  width:3px;height:auto;align-self:stretch;flex-shrink:0;
}
.service-card.featured .service-body{
  flex:1;display:flex;align-items:center;gap:2rem;padding:1.4rem 1.6rem;
}
.service-card.featured .service-agent-row{margin-bottom:0;flex-shrink:0}
.service-card.featured .service-photo{width:84px;height:84px}
.service-card.featured .service-content{flex:1}
.service-card.featured h3{font-size:1.1rem;margin-bottom:.35rem}
.service-card.featured .service-footer{margin-top:.8rem;padding-top:.6rem}
.service-card.featured .service-agent-name{font-size:.9rem}
.service-card.featured .service-agent-role{font-size:.72rem}

/* ════════════════════════════════════════════════════════════
   TEAM
═══════════════════════════════════════════════════════════ */
.team-grid{
  display:grid;grid-template-columns:repeat(4,1fr);
  gap:1rem;margin-top:3rem;
}
.team-card{
  background:var(--ebony-2);
  border:1px solid var(--gold-line);
  border-radius:6px;
  padding:1.4rem 1.2rem;
  text-align:center;
  transition:transform .2s,border-color .2s;
  position:relative;overflow:hidden;
}
.team-card::before{
  content:'';position:absolute;top:0;left:0;right:0;height:1px;
  background:linear-gradient(90deg,transparent,var(--ochre),transparent);
  opacity:0;transition:opacity .2s;
}
.team-card:hover{transform:translateY(-3px);border-color:rgba(201,125,32,.45)}
.team-card:hover::before{opacity:1}
.team-avatar{
  width:130px;height:130px;border-radius:50%;
  border:2px solid var(--gold-line);
  margin:0 auto 1.2rem;
  overflow:hidden;
  background:var(--ebony-4);
  box-shadow:0 0 0 5px rgba(201,125,32,.1);
  transition:box-shadow .25s,border-color .25s;
}
.team-card:hover .team-avatar{
  border-color:var(--ochre);
  box-shadow:0 0 0 5px rgba(201,125,32,.2);
}
.team-avatar img{
  width:100%;height:100%;
  object-fit:cover;object-position:top center;
  display:block;
}
.team-name{
  font-family:'Playfair Display',serif;
  font-size:.95rem;font-weight:700;color:var(--cream);
  margin-bottom:.2rem;
}
.team-role{font-size:.72rem;color:var(--ochre);letter-spacing:.05em;text-transform:uppercase;margin-bottom:.6rem}
.team-desc{font-size:.78rem;color:var(--cream-dim);line-height:1.55}
/* featured orchestrator card spans 2 columns and is wider */
.team-card.featured{
  grid-column:span 2;
  display:flex;gap:1.6rem;align-items:flex-start;
  text-align:left;
}
.team-card.featured .team-avatar{
  flex-shrink:0;
  width:170px;height:170px;
  margin:0;
}
.team-card.featured .team-name{font-size:1.15rem}

/* ════════════════════════════════════════════════════════════
   BRIEF FORM
═══════════════════════════════════════════════════════════ */
.form-section{
  background:var(--ebony-2);
  border:1px solid var(--gold-line);
  border-radius:8px;
  padding:3rem;
  position:relative;overflow:hidden;
}
.form-section::before{
  content:'';position:absolute;top:0;left:0;right:0;height:2px;
  background:linear-gradient(90deg,var(--terra),var(--ochre),var(--green-l));
}
.form-grid{display:grid;grid-template-columns:1fr 1fr;gap:1.2rem}
.form-grid .full{grid-column:1/-1}
.field label{
  display:block;font-size:.72rem;font-weight:600;
  letter-spacing:.07em;text-transform:uppercase;
  color:var(--ochre);margin-bottom:.45rem;
}
.field input,.field textarea,.field select{
  width:100%;
  background:var(--ebony-3);
  border:1px solid var(--gold-line);
  border-radius:4px;
  padding:.7rem 1rem;
  font-size:.9rem;
  font-family:'DM Sans',sans-serif;
  color:var(--cream);
  transition:border-color .2s,box-shadow .2s;
  outline:none;
}
.field input::placeholder,.field textarea::placeholder{color:rgba(245,237,216,.28)}
.field input:focus,.field textarea:focus{
  border-color:var(--ochre);
  box-shadow:0 0 0 3px rgba(201,125,32,.12);
}
.field textarea{resize:vertical;min-height:82px}
.req{color:var(--terra)}
.form-submit{
  width:100%;margin-top:1.5rem;
  background:var(--terra);color:#fff;
  border:none;border-radius:4px;cursor:pointer;
  padding:1rem;font-size:1rem;font-weight:600;
  font-family:'DM Sans',sans-serif;
  letter-spacing:.04em;
  transition:background .2s,transform .15s;
}
.form-submit:hover{background:var(--terra-d);transform:translateY(-1px)}
.form-submit:disabled{opacity:.45;cursor:not-allowed;transform:none}

/* Status box */
.status-box{
  margin-top:1.2rem;border-radius:4px;
  padding:.95rem 1.2rem;font-size:.88rem;
  display:none;
}
.s-running{background:rgba(201,125,32,.1);border:1px solid rgba(201,125,32,.3);color:var(--ochre-l)}
.s-done   {background:rgba(30,77,43,.2);border:1px solid rgba(42,107,60,.5);color:#7FD4A0}
.s-error  {background:rgba(192,71,42,.12);border:1px solid rgba(192,71,42,.4);color:#E07560}

.spinner{
  display:inline-block;width:13px;height:13px;
  border:2px solid currentColor;border-top-color:transparent;
  border-radius:50%;vertical-align:middle;margin-right:.5rem;
  animation:spin .75s linear infinite;
}
@keyframes spin{to{transform:rotate(360deg)}}

.result-links{display:flex;gap:.8rem;flex-wrap:wrap;margin-top:.9rem}
.link-btn{
  display:inline-block;padding:.4rem 1rem;
  border-radius:3px;font-size:.8rem;font-weight:600;
  text-decoration:none;letter-spacing:.04em;
}
.link-btn.terra{background:var(--terra);color:#fff}
.link-btn.ochre{background:transparent;border:1px solid var(--ochre);color:var(--ochre)}

/* ════════════════════════════════════════════════════════════
   CAMPAIGN RUNS TABLE
═══════════════════════════════════════════════════════════ */
.runs-table-wrap{overflow-x:auto;margin-top:2rem}
table{width:100%;border-collapse:collapse;font-size:.84rem}
thead th{
  background:var(--ebony-3);
  border-bottom:1px solid var(--gold-line);
  padding:.65rem 1rem;
  text-align:left;
  font-size:.7rem;font-weight:600;
  text-transform:uppercase;letter-spacing:.07em;
  color:var(--cream-dim);
}
tbody td{
  padding:.65rem 1rem;
  border-bottom:1px solid rgba(201,125,32,.08);
  color:var(--cream);
  vertical-align:middle;
}
tbody tr:last-child td{border-bottom:none}
tbody tr:hover td{background:rgba(201,125,32,.04)}
.badge{
  display:inline-block;border-radius:2px;
  padding:.15rem .6rem;font-size:.7rem;font-weight:700;
  letter-spacing:.05em;text-transform:uppercase;
}
.b-running{background:rgba(201,125,32,.18);color:var(--ochre-l)}
.b-done{background:rgba(30,77,43,.35);color:#7FD4A0}
.b-error{background:rgba(192,71,42,.2);color:#E07560}
.t-link{color:var(--ochre);text-decoration:none;font-weight:600;font-size:.78rem}
.t-link:hover{color:var(--ochre-l)}
.empty-state{
  text-align:center;padding:3rem;
  color:var(--cream-dim);font-size:.88rem;
  border:1px dashed var(--gold-line);
  border-radius:6px;margin-top:1.5rem;
  font-style:italic;
}

/* ════════════════════════════════════════════════════════════
   FOOTER
═══════════════════════════════════════════════════════════ */
footer{
  background:var(--ebony-2);
  border-top:1px solid var(--gold-line);
  padding:3rem 2rem 2rem;
  position:relative;z-index:1;
}
.footer-inner{
  max-width:1180px;margin:0 auto;
  display:grid;grid-template-columns:1.4fr 1fr 1fr;gap:3rem;
}
.footer-brand .nav-logo{display:flex;align-items:center;gap:.75rem;margin-bottom:.8rem;text-decoration:none;}
.footer-brand .nav-logo-img{width:40px;height:40px;border-radius:50%;object-fit:cover;border:1.5px solid rgba(201,125,32,.45);background:#000;flex-shrink:0;}
.footer-brand .nav-logo-text{font-family:'Playfair Display',serif;font-size:1.25rem;font-weight:700;color:var(--ochre);}
.footer-brand p{font-size:.84rem;color:var(--cream-dim);line-height:1.7;max-width:280px}
.footer-col h4{
  font-size:.72rem;font-weight:600;letter-spacing:.1em;
  text-transform:uppercase;color:var(--ochre);margin-bottom:1rem;
}
.footer-col ul{list-style:none}
.footer-col ul li{margin-bottom:.5rem}
.footer-col ul a{
  color:var(--cream-dim);font-size:.84rem;text-decoration:none;
  transition:color .2s;
}
.footer-col ul a:hover{color:var(--cream)}
.footer-bottom{
  max-width:1180px;margin:2rem auto 0;
  padding-top:1.5rem;border-top:1px solid var(--gold-line);
  display:flex;justify-content:space-between;align-items:center;
  font-size:.75rem;color:var(--cream-dim);
  flex-wrap:wrap;gap:.5rem;
}
.kente-small{
  height:4px;
  background:repeating-linear-gradient(
    90deg,
    var(--ochre) 0,var(--ochre) 8px,
    var(--terra) 8px,var(--terra) 16px,
    var(--green) 16px,var(--green) 24px,
    var(--ebony) 24px,var(--ebony) 26px
  );
  margin-bottom:2rem;
}

/* ════════════════════════════════════════════════════════════
   JSON VIEWER
═══════════════════════════════════════════════════════════ */
.json-pre{
  background:var(--ebony);
  border:1px solid var(--gold-line);
  border-radius:6px;
  padding:1.4rem;
  font-family:'Fira Code','Cascadia Code',monospace;
  font-size:.76rem;color:#A6E3A1;
  line-height:1.65;
  overflow:auto;max-height:440px;
  white-space:pre;
  margin-top:1.2rem;display:none;
}

/* ── Solo mode banner ───────────────────────────────────── */
.solo-banner{
  display:none;align-items:center;gap:1rem;
  background:rgba(201,125,32,.07);
  border:1px solid rgba(201,125,32,.35);
  border-radius:5px;padding:.75rem 1.1rem;
  margin-bottom:1.6rem;
}
.solo-banner-icon{
  width:38px;height:38px;border-radius:50%;
  overflow:hidden;flex-shrink:0;
  border:1px solid var(--gold-line);background:var(--ebony-4);
}
.solo-banner-icon img{width:100%;height:100%;object-fit:cover;object-position:top center;display:block}
.solo-banner-text{flex:1}
.solo-banner-label{font-size:.66rem;color:var(--cream-dim);letter-spacing:.08em;text-transform:uppercase;margin-bottom:.1rem}
.solo-banner-name{font-size:.88rem;font-weight:600;color:var(--ochre);font-family:'Playfair Display',serif}
.solo-clear-btn{
  background:transparent;border:1px solid rgba(192,71,42,.4);
  color:var(--terra);border-radius:3px;
  padding:.22rem .7rem;font-size:.7rem;font-weight:600;
  letter-spacing:.05em;text-transform:uppercase;cursor:pointer;
  font-family:'DM Sans',sans-serif;
  transition:background .15s,border-color .15s,color .15s;
  white-space:nowrap;
}
.solo-clear-btn:hover{background:rgba(192,71,42,.12);border-color:var(--terra);color:#E07560}

/* ── Responsive ─────────────────────────────────────────── */
@media(max-width:960px){
  .hero-grid{grid-template-columns:1fr;gap:2.5rem}
  .services-grid{grid-template-columns:1fr 1fr}
  .team-grid{grid-template-columns:1fr 1fr}
  .team-card.featured{grid-column:span 2}
  .footer-inner{grid-template-columns:1fr}
}
@media(max-width:640px){
  nav{padding:.8rem 1.2rem}
  .nav-links{display:none}
  .services-grid,.team-grid{grid-template-columns:1fr}
  .team-card.featured{grid-column:span 1;flex-direction:column}
  .form-grid{grid-template-columns:1fr}
  .form-grid .full{grid-column:1}
  .form-section{padding:1.8rem}
  .section{padding:3.5rem 1.2rem}
}
</style>
</head>

<body>

<!-- ── Kente border ────────────────────────────────────────── -->
<div class="kente"></div>

<!-- ── Navigation ─────────────────────────────────────────── -->
<nav>
  <a href="#" class="nav-logo">
    <img src="/static/logo.png" alt="Teranga" class="nav-logo-img"/>
    <span class="nav-logo-text">TERANGA<span> Agency</span></span>
  </a>
  <ul class="nav-links">
    <li><a href="#services">Services</a></li>
    <li><a href="#team">The Team</a></li>
    <li><a href="#campaign">Launch</a></li>
    <li><a href="#runs">Campaigns</a></li>
    <li><a href="/docs" target="_blank">API</a></li>
  </ul>
  <a href="#campaign" class="nav-cta">New Campaign</a>
</nav>

<!-- ════════════════════════════════════════════════════════
     HERO
═══════════════════════════════════════════════════════ -->
<div class="hero-wrap">
  <img src="/static/logo.png" class="logo-bg" alt=""/>
  <div class="hero-grid">

    <!-- LEFT -->
    <div class="hero-left">
      <!-- Hero Logo Mark -->
      <div style="margin-bottom:1.6rem;display:flex;align-items:center;gap:1.1rem;">
        <img src="/static/logo.png" alt="Teranga Agency Logo"
             style="width:72px;height:72px;border-radius:50%;object-fit:cover;
                    border:2px solid rgba(201,125,32,.55);
                    box-shadow:0 0 24px rgba(201,125,32,.3),0 0 0 6px rgba(201,125,32,.07);
                    background:#000;flex-shrink:0;"/>
        <div>
          <div style="font-family:'Playfair Display',serif;font-size:1.1rem;font-weight:700;color:var(--ochre);letter-spacing:.5px;">TERANGA AGENCY</div>
          <div style="font-size:.72rem;color:var(--cream-dim);letter-spacing:.1em;text-transform:uppercase;margin-top:.15rem;">AI · Strategy · Growth</div>
        </div>
      </div>

      <div class="hero-tag">
        West African AI Intelligence
      </div>
      <h1>
        Seven Minds.<br/>
        One <em>Campaign.</em>
      </h1>
      <p class="hero-desc">
        Teranga is a multi-agent AI marketing agency powered by 7 specialists —
        each named after a great tradition of Senegalese excellence. Give us a brief,
        we deliver a complete campaign: strategy, content, visuals, video, KPIs, and report.
      </p>
      <div class="hero-ctas">
        <a href="#campaign" class="btn-primary">Launch a Campaign</a>
        <a href="#team" class="btn-ghost">Meet the Team</a>
      </div>
      <div class="hero-social-proof">
        <div class="proof-stat">
          <span class="proof-num">7</span>
          <span class="proof-label">AI Specialists</span>
        </div>
        <div class="proof-stat">
          <span class="proof-num">8</span>
          <span class="proof-label">Deliverables</span>
        </div>
        <div class="proof-stat">
          <span class="proof-num">&lt;8m</span>
          <span class="proof-label">Per Campaign</span>
        </div>
      </div>
    </div>

    <!-- RIGHT: Dashboard Card -->
    <div>
      <div class="dashboard-card">
        <div class="dash-header">
          <span class="dash-title">Campaign Dashboard</span>
          <span class="dash-live"><span class="live-dot"></span>Live</span>
        </div>

        <div class="dash-metrics">
          <div class="metric-box">
            <div class="metric-label">Campaign ROI</div>
            <div class="metric-val" id="m-roi">0%</div>
            <div class="metric-change">↑ vs last quarter</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">Total Reach</div>
            <div class="metric-val green" id="m-reach">0</div>
            <div class="metric-change">↑ organic + paid</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">Pre-orders</div>
            <div class="metric-val terra" id="m-orders">0</div>
            <div class="metric-change">↑ vs target 500</div>
          </div>
          <div class="metric-box">
            <div class="metric-label">Engagement</div>
            <div class="metric-val" id="m-eng">0%</div>
            <div class="metric-change">↑ industry avg 2.1%</div>
          </div>
        </div>

        <div>
          <div class="dash-bar-label"><span>Instagram Followers</span><span>10K goal</span></div>
          <div class="dash-bar-track"><div class="dash-bar-fill" style="--w:72%;background:linear-gradient(90deg,var(--terra),var(--ochre))"></div></div>
          <div class="dash-bar-label"><span>Email Conversions</span><span>35% open rate</span></div>
          <div class="dash-bar-track"><div class="dash-bar-fill" style="--w:87%;background:linear-gradient(90deg,var(--green),#4CAF79)"></div></div>
          <div class="dash-bar-label"><span>Paid Ad ROAS</span><span>4.2× target</span></div>
          <div class="dash-bar-track"><div class="dash-bar-fill" style="--w:94%;background:linear-gradient(90deg,var(--ochre-d),var(--ochre-l))"></div></div>
        </div>

        <div class="dash-agents">
          <div class="dash-agents-title">Agent Status</div>
          <div class="agent-row"><span class="agent-dot" style="background:var(--ochre)"></span><span class="agent-name">Ibrahima Sow</span><span class="agent-status">Strategy ✓</span></div>
          <div class="agent-row"><span class="agent-dot" style="background:var(--terra)"></span><span class="agent-name">Aminata Diallo</span><span class="agent-status">Writing copy…</span></div>
          <div class="agent-row"><span class="agent-dot" style="background:var(--green-l)"></span><span class="agent-name">Rokhaya Ndiaye</span><span class="agent-status idle">Queued</span></div>
          <div class="agent-row"><span class="agent-dot" style="background:var(--cream-d)"></span><span class="agent-name">Samba Mbaye</span><span class="agent-status idle">Queued</span></div>
        </div>
      </div>
    </div>

  </div><!-- /hero-grid -->
</div><!-- /hero-wrap -->

<!-- ── Stats bar ──────────────────────────────────────────── -->
<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat-item">
      <span class="stat-num">847%</span>
      <span class="stat-label">Average Campaign ROI</span>
    </div>
    <div class="stat-sep"></div>
    <div class="stat-item">
      <span class="stat-num">2.4M</span>
      <span class="stat-label">Total Reach Delivered</span>
    </div>
    <div class="stat-sep"></div>
    <div class="stat-item">
      <span class="stat-num">12K+</span>
      <span class="stat-label">Conversions Generated</span>
    </div>
    <div class="stat-sep"></div>
    <div class="stat-item">
      <span class="stat-num">8.3%</span>
      <span class="stat-label">Avg. Engagement Rate</span>
    </div>
    <div class="stat-sep"></div>
    <div class="stat-item">
      <span class="stat-num">3–8m</span>
      <span class="stat-label">Campaign Runtime</span>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- ════════════════════════════════════════════════════════
     SERVICES
═══════════════════════════════════════════════════════ -->
<div class="section" id="services">
  <div class="eyebrow">What We Deliver</div>
  <h2>Eight deliverables.<br/><em class="italic gold">Every campaign.</em></h2>

  <div class="services-grid">

    <!-- Featured: Cheikh — Orchestrator -->
    <div class="service-card featured">
      <div class="service-top ochre" style="background:linear-gradient(180deg,var(--ochre-d),var(--ochre-l))"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/cheikh.png" alt="Cheikh Diagne"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Cheikh Diagne</div>
            <div class="service-agent-role">Campaign Orchestrator</div>
          </div>
        </div>
        <div class="service-content">
          <h3>Full Campaign Assembly</h3>
          <p>Cheikh synthesises every agent's output into a single structured JSON payload — social posts, email sequences, ad copies, image prompts, video scripts, and KPIs — ready for your CMS or Supabase.</p>
          <div class="service-footer">
            <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included · JSON output</span>
            <button class="service-solo-btn" onclick="selectSolo('orchestrator')">Run Solo →</button>
          </div>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top ochre"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/ibrahima.png" alt="Ibrahima Sow"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Ibrahima Sow</div>
            <div class="service-agent-role">Strategist</div>
          </div>
        </div>
        <h3>Marketing Strategy</h3>
        <p>Full go-to-market strategy — target audience, competitive positioning, channel mix, budget allocation, and 90-day roadmap.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('strategist')">Run Solo →</button>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top terra"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/aminata.png" alt="Aminata Diallo"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Aminata Diallo</div>
            <div class="service-agent-role">Content Creator</div>
          </div>
        </div>
        <h3>Social Media Content</h3>
        <p>Platform-native posts for Instagram, LinkedIn, X, and Facebook — fully written captions, hashtags, and CTAs.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('content_creator')">Run Solo →</button>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top green"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/rokhaya.png" alt="Rokhaya Ndiaye"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Rokhaya Ndiaye</div>
            <div class="service-agent-role">Visual Designer</div>
          </div>
        </div>
        <h3>Image Generation Prompts</h3>
        <p>Six detailed, production-ready prompts for Midjourney and DALL-E — hero banners, social posts, ads, and email headers.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('visual_designer')">Run Solo →</button>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top ochre"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/samba.png" alt="Samba Mbaye"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Samba Mbaye</div>
            <div class="service-agent-role">Video Scriptwriter</div>
          </div>
        </div>
        <h3>Video Scripts</h3>
        <p>A 60-second brand film and a 15-second short-form video — full scene direction, voiceover, text overlays, and music notes.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('video_writer')">Run Solo →</button>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top terra"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/ousmane.png" alt="Ousmane Faye"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Ousmane Faye</div>
            <div class="service-agent-role">Analyst</div>
          </div>
        </div>
        <h3>KPI & Analytics Framework</h3>
        <p>12 KPIs mapped to funnel stages, reporting cadence, tool stack recommendations, and a 30-day A/B testing plan.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('analyst')">Run Solo →</button>
        </div>
      </div>
    </div>

    <div class="service-card">
      <div class="service-top green"></div>
      <div class="service-body">
        <div class="service-agent-row">
          <div class="service-photo"><img src="/static/fatou.png" alt="Fatou Sarr"/></div>
          <div class="service-agent-info">
            <div class="service-agent-name">Fatou Sarr</div>
            <div class="service-agent-role">Presenter</div>
          </div>
        </div>
        <h3>Client Report</h3>
        <p>A polished client-ready Markdown report and a Supabase-ready JSON payload — structured, complete, and ready to present.</p>
        <div class="service-footer">
          <span style="font-size:.72rem;color:var(--cream-dim)">Full campaign included</span>
          <button class="service-solo-btn" onclick="selectSolo('presenter')">Run Solo →</button>
        </div>
      </div>
    </div>

  </div>
</div>

<div class="divider"></div>

<!-- ════════════════════════════════════════════════════════
     TEAM
═══════════════════════════════════════════════════════ -->
<div class="section" id="team">
  <div class="eyebrow">The Teranga Seven</div>
  <h2>Named after Senegal's<br/><em class="italic gold">greatest traditions.</em></h2>

  <div class="team-grid">

    <!-- Featured: Cheikh -->
    <div class="team-card featured">
      <div class="team-avatar">
        <img src="/static/cheikh.png" alt="Cheikh Diagne"/>
      </div>
      <div>
        <div class="team-name">Cheikh Diagne</div>
        <div class="team-role">Campaign Orchestrator</div>
        <div class="team-desc">Cheikh — meaning "wise elder" in Wolof — is the calm center of every campaign. He grew up watching his grandfather broker trade at Sandaga market. Nothing ships without his signature.</div>
      </div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/ibrahima.png" alt="Ibrahima Sow"/>
      </div>
      <div class="team-name">Ibrahima Sow</div>
      <div class="team-role">Marketing Strategist</div>
      <div class="team-desc">Debated economics under Saint-Louis baobab trees. HEC Paris. McKinsey Johannesburg. Brands that work with Ibrahima don't just grow — they own their category.</div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/aminata.png" alt="Aminata Diallo"/>
      </div>
      <div class="team-name">Aminata Diallo</div>
      <div class="team-role">Content Creator</div>
      <div class="team-desc">Grew up hearing her grandmother tell stories in Wolof that made the whole neighborhood stop. She inherited that gift. Her email sequences have generated millions in revenue.</div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/rokhaya.png" alt="Rokhaya Ndiaye"/>
      </div>
      <div class="team-name">Rokhaya Ndiaye</div>
      <div class="team-role">Visual Prompt Designer</div>
      <div class="team-desc">Was painting murals on Dakar's Plateau walls before she touched a computer. Trained in Gorée Island. Her prompts are so precise designers call them "visual blueprints."</div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/samba.png" alt="Samba Mbaye"/>
      </div>
      <div class="team-name">Samba Mbaye</div>
      <div class="team-role">Video Scriptwriter</div>
      <div class="team-desc">From a long line of griots — West Africa's oral historians. Took that ancient storytelling to film school in Nairobi, then ad agencies in Lagos and New York.</div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/ousmane.png" alt="Ousmane Faye"/>
      </div>
      <div class="team-name">Ousmane Faye</div>
      <div class="team-role">Marketing Analyst</div>
      <div class="team-desc">Solved math puzzles in Thiès, finished top of his class at Université Cheikh Anta Diop. Built analytics at Jumia. Every number he tracks is tied to a business outcome.</div>
    </div>

    <div class="team-card">
      <div class="team-avatar">
        <img src="/static/fatou.png" alt="Fatou Sarr"/>
      </div>
      <div class="team-name">Fatou Sarr</div>
      <div class="team-role">Presentation Agent</div>
      <div class="team-desc">Daughter of a diplomat, attended her first state dinner at twelve. Sciences Po Paris. A decade at Publicis. Her reports are legendary for clarity, completeness, and professionalism.</div>
    </div>

  </div>
</div>

<div class="divider"></div>

<!-- ════════════════════════════════════════════════════════
     CAMPAIGN BRIEF FORM
═══════════════════════════════════════════════════════ -->
<div class="section" id="campaign">
  <div class="eyebrow">Start a Campaign</div>
  <h2>Give us your brief.<br/><em class="italic gold">We do the rest.</em></h2>

  <div style="margin-top:2.5rem">
    <div class="form-section">
      <!-- Solo mode indicator (hidden by default) -->
      <div id="soloModeBanner" class="solo-banner">
        <div class="solo-banner-icon"><img id="soloBannerImg" src="" alt=""/></div>
        <div class="solo-banner-text">
          <div class="solo-banner-label">Solo Mode — one specialist</div>
          <div class="solo-banner-name" id="soloBannerName"></div>
        </div>
        <button type="button" class="solo-clear-btn" onclick="clearSolo()">✕ Full Campaign</button>
      </div>

      <form id="briefForm">
        <div class="form-grid">
          <div class="field">
            <label>Client Name <span class="req">*</span></label>
            <input name="client_name" placeholder="e.g. EcoWear" required/>
          </div>
          <div class="field">
            <label>Industry <span class="req">*</span></label>
            <input name="industry" placeholder="e.g. Sustainable Fashion" required/>
          </div>
          <div class="field full">
            <label>Product / Service <span class="req">*</span></label>
            <input name="product_service" placeholder="What exactly are you selling or promoting?" required/>
          </div>
          <div class="field full">
            <label>Target Audience <span class="req">*</span></label>
            <textarea name="target_audience" placeholder="Demographics, psychographics, behaviors, platforms they use…" required></textarea>
          </div>
          <div class="field full">
            <label>Campaign Objective <span class="req">*</span></label>
            <textarea name="campaign_objective" placeholder="What does success look like? Be specific — numbers, timelines…" required></textarea>
          </div>
          <div class="field">
            <label>Budget</label>
            <input name="budget" placeholder="e.g. $15,000 USD"/>
          </div>
          <div class="field">
            <label>Timeline</label>
            <input name="timeline" placeholder="e.g. 6 weeks"/>
          </div>
          <div class="field full">
            <label>Unique Selling Proposition <span class="req">*</span></label>
            <textarea name="unique_selling_proposition" placeholder="What makes you irreplaceable? What can no competitor authentically claim?" required></textarea>
          </div>
          <div class="field">
            <label>Competitors</label>
            <input name="competitors" placeholder="e.g. Brand A, Brand B, Brand C"/>
          </div>
          <div class="field">
            <label>Tone of Voice</label>
            <input name="tone_of_voice" placeholder="e.g. Bold, authentic — never preachy"/>
          </div>
          <div class="field full">
            <label>Additional Notes</label>
            <textarea name="additional_notes" placeholder="Brand colors, founder story, past campaigns, key constraints, anything else…"></textarea>
          </div>
        </div>
        <button type="submit" class="form-submit" id="submitBtn">
          Launch the Teranga Seven →
        </button>
      </form>
      <div id="statusBox" class="status-box"></div>
    </div>
  </div>
</div>

<div class="divider"></div>

<!-- ════════════════════════════════════════════════════════
     CAMPAIGN RUNS
═══════════════════════════════════════════════════════ -->
<div class="section" id="runs">
  <div class="eyebrow">Campaign Runs</div>
  <h2>Results &amp; <em class="italic gold">History</em></h2>
  <div id="runsTable"></div>
  <div id="resultJson" class="json-pre"></div>
</div>

<!-- ── Kente footer strip ─────────────────────────────────── -->
<div class="kente-small"></div>

<!-- ════════════════════════════════════════════════════════
     FOOTER
═══════════════════════════════════════════════════════ -->
<footer>
  <div class="footer-inner">
    <div class="footer-brand">
      <a href="#" class="nav-logo">
        <img src="/static/logo.png" alt="Teranga" class="nav-logo-img"/>
        <span class="nav-logo-text">TERANGA<span> Agency</span></span>
      </a>
      <p>Seven AI specialists, each rooted in the spirit of Senegalese excellence, delivering complete marketing campaigns from a single brief.</p>
    </div>
    <div class="footer-col">
      <h4>Deliverables</h4>
      <ul>
        <li><a href="#services">Marketing Strategy</a></li>
        <li><a href="#services">Social Media Content</a></li>
        <li><a href="#services">Email Sequences</a></li>
        <li><a href="#services">Ad Copy</a></li>
        <li><a href="#services">Image Prompts</a></li>
        <li><a href="#services">Video Scripts</a></li>
        <li><a href="#services">KPI Framework</a></li>
      </ul>
    </div>
    <div class="footer-col">
      <h4>Developer</h4>
      <ul>
        <li><a href="/docs" target="_blank">Swagger API Docs</a></li>
        <li><a href="/redoc" target="_blank">ReDoc Reference</a></li>
        <li><a href="/api/outputs" target="_blank">Campaign Outputs</a></li>
        <li><a href="/api/campaigns" target="_blank">Active Runs</a></li>
      </ul>
    </div>
  </div>
  <div class="footer-bottom">
    <span>© 2026 Teranga AI Marketing Agency · «L'hospitalité au service de votre marque»</span>
    <span>Cheikh · Ibrahima · Aminata · Rokhaya · Samba · Ousmane · Fatou</span>
  </div>
</footer>

<script>
/* ── Counter animation ─────────────────────────────── */
function animateCount(el, end, suffix='', duration=1800) {
  let start = 0, step = end / (duration / 16);
  const tick = () => {
    start = Math.min(start + step, end);
    el.textContent = (start >= 1000
      ? (start/1000).toFixed(start >= 10000 ? 0 : 1) + 'K'
      : Math.round(start)) + suffix;
    if (start < end) requestAnimationFrame(tick);
  };
  requestAnimationFrame(tick);
}
window.addEventListener('load', () => {
  setTimeout(() => {
    animateCount(document.getElementById('m-roi'), 847, '%');
    animateCount(document.getElementById('m-reach'), 2400000, '');
    animateCount(document.getElementById('m-orders'), 512, '');
    animateCount(document.getElementById('m-eng'), 8.3, '%', 1400);
  }, 600);
});

/* ── Solo agent mode ──────────────────────────────── */
const AGENT_LABELS = {
  strategist:      { name:'Ibrahima Sow',   role:'Marketing Strategist',  img:'ibrahima' },
  content_creator: { name:'Aminata Diallo', role:'Content Creator',       img:'aminata'  },
  visual_designer: { name:'Rokhaya Ndiaye', role:'Visual Designer',       img:'rokhaya'  },
  video_writer:    { name:'Samba Mbaye',    role:'Video Scriptwriter',    img:'samba'    },
  analyst:         { name:'Ousmane Faye',   role:'Marketing Analyst',     img:'ousmane'  },
  presenter:       { name:'Fatou Sarr',     role:'Presentation Agent',    img:'fatou'    },
  orchestrator:    { name:'Cheikh Diagne',  role:'Campaign Orchestrator', img:'cheikh'   },
};
let soloAgent = null;

function selectSolo(agentKey) {
  const info = AGENT_LABELS[agentKey];
  if (!info) return;
  soloAgent = agentKey;
  document.getElementById('soloBannerImg').src = `/static/${info.img}.png`;
  document.getElementById('soloBannerImg').alt = info.name;
  document.getElementById('soloBannerName').textContent = `${info.name} — ${info.role}`;
  document.getElementById('soloModeBanner').style.display = 'flex';
  submitBtn.textContent = `Run ${info.name} Solo →`;
  document.getElementById('campaign').scrollIntoView({behavior:'smooth'});
}

function clearSolo() {
  soloAgent = null;
  document.getElementById('soloModeBanner').style.display = 'none';
  submitBtn.textContent = 'Launch the Teranga Seven →';
}

/* ── Form ─────────────────────────────────────────── */
const form      = document.getElementById('briefForm');
const statusBox = document.getElementById('statusBox');
const submitBtn = document.getElementById('submitBtn');
const runsTable = document.getElementById('runsTable');
const resultJson= document.getElementById('resultJson');

let pollInterval = null, timerInterval = null;
let startedAt = 0;

form.addEventListener('submit', async e => {
  e.preventDefault();
  const data = Object.fromEntries(
    [...new FormData(form).entries()].filter(([,v]) => v.trim())
  );
  if (soloAgent) data.selected_agents = [soloAgent];
  submitBtn.disabled = true;
  startedAt = Date.now();
  const runningMsg = soloAgent
    ? `${AGENT_LABELS[soloAgent].name} is working on your brief…`
    : 'The Teranga Seven are working on your campaign…';
  showRunning(runningMsg);

  try {
    const res = await fetch('/api/campaigns', {
      method: 'POST',
      headers: {'Content-Type':'application/json'},
      body: JSON.stringify(data)
    });
    if (!res.ok) throw new Error(`Server error ${res.status}: ${await res.text()}`);
    const job = await res.json();
    startPolling(job.campaign_id);
  } catch(err) {
    showStatus('error', '✗ ' + err.message);
    submitBtn.disabled = false;
    clearInterval(timerInterval);
  }
});

function showRunning(msg) {
  showStatus('running',
    `<span class="spinner"></span>${msg} &nbsp;<span id="elapsed" style="opacity:.6;font-size:.8rem"></span>`
  );
  clearInterval(timerInterval);
  timerInterval = setInterval(() => {
    const s = Math.floor((Date.now()-startedAt)/1000);
    const el = document.getElementById('elapsed');
    if (el) el.textContent = `${String(Math.floor(s/60)).padStart(2,'0')}:${String(s%60).padStart(2,'0')} elapsed`;
  }, 1000);
}

function showStatus(type, html) {
  statusBox.className = 'status-box s-' + type;
  statusBox.innerHTML = html;
  statusBox.style.display = 'block';
}

function startPolling(id) {
  if (pollInterval) clearInterval(pollInterval);
  pollStatus(id);
  pollInterval = setInterval(() => pollStatus(id), 5000);
}

async function pollStatus(id) {
  try {
    const res = await fetch('/api/campaigns/' + id);
    if (!res.ok) return;
    const job = await res.json();
    if (job.status === 'done') {
      clearInterval(pollInterval); clearInterval(timerInterval);
      const s = Math.floor((Date.now()-startedAt)/1000);
      showStatus('done', `✓ Campaign complete for <strong>${job.client_name}</strong> — ${Math.floor(s/60)}m ${s%60}s
        <div class="result-links">
          <a class="link-btn terra" href="/api/campaigns/${id}/result" target="_blank">JSON Payload</a>
          <a class="link-btn ochre" href="/api/campaigns/${id}/report" target="_blank">Markdown Report</a>
        </div>`);
      submitBtn.disabled = false;
      fetchResult(id); loadRuns();
    } else if (job.status === 'error') {
      clearInterval(pollInterval); clearInterval(timerInterval);
      showStatus('error', `✗ Campaign failed. <a href="/api/campaigns/${id}/error" target="_blank" style="color:inherit;font-weight:700;text-decoration:underline">View error traceback →</a>`);
      submitBtn.disabled = false;
    }
  } catch(e) {}
}

async function fetchResult(id) {
  try {
    const data = await fetch('/api/campaigns/'+id+'/result').then(r=>r.json());
    resultJson.textContent = JSON.stringify(data, null, 2);
    resultJson.style.display = 'block';
    resultJson.scrollIntoView({behavior:'smooth',block:'nearest'});
  } catch(e) {}
}

async function loadRuns() {
  try {
    const [jobs, outputs] = await Promise.all([
      fetch('/api/campaigns').then(r=>r.json()),
      fetch('/api/outputs').then(r=>r.json())
    ]);
    const all = [
      ...jobs.map(j=>({...j})),
      ...outputs.filter(o=>!jobs.find(j=>j.campaign_id===o.campaign_id))
               .map(o=>({...o, status:'done'}))
    ];
    if (!all.length) {
      runsTable.innerHTML = '<div class="empty-state">No campaigns yet — submit a brief above to get started.</div>';
      return;
    }
    runsTable.innerHTML = `<div class="runs-table-wrap"><table>
      <thead><tr>
        <th>Client</th><th>Status</th><th>Started</th>
        <th>Posts</th><th>Emails</th><th>KPIs</th><th>Actions</th>
      </tr></thead>
      <tbody>${all.map(r=>`<tr>
        <td>
          <strong style="color:var(--cream)">${r.client_name}</strong><br/>
          <span style="font-size:.72rem;color:var(--cream-dim);font-family:monospace">${r.campaign_id.slice(0,12)}…</span>
        </td>
        <td><span class="badge b-${r.status}">${r.status}</span></td>
        <td style="font-size:.78rem;color:var(--cream-dim)">${(r.started_at||r.created_at||'').slice(0,16).replace('T',' ')}</td>
        <td style="color:var(--ochre);font-weight:600">${r.social_posts??'—'}</td>
        <td style="color:var(--ochre);font-weight:600">${r.emails??'—'}</td>
        <td style="color:var(--ochre);font-weight:600">${r.kpis??'—'}</td>
        <td>${r.status==='done'
          ? `<a class="t-link" href="/api/campaigns/${r.campaign_id}/result" target="_blank">JSON</a>
             &nbsp;·&nbsp;
             <a class="t-link" href="/api/campaigns/${r.campaign_id}/report" target="_blank">Report</a>`
          : r.status==='error'
          ? `<a class="t-link" href="/api/campaigns/${r.campaign_id}/error" target="_blank" style="color:var(--terra)">Error</a>`
          : '<span style="color:var(--cream-dim);font-size:.78rem">Running…</span>'}</td>
      </tr>`).join('')}</tbody>
    </table></div>`;
  } catch(e) {}
}

loadRuns();
</script>
</body>
</html>"""


@ui_router.get("/", response_class=HTMLResponse)
async def index():
    return HTMLResponse(content=HTML)
