#!/usr/bin/env python3
"""
TERANGA AGENCY — Premium PDF Report Generator
"""
import math
from pathlib import Path
from datetime import datetime

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm, cm
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_RIGHT, TA_JUSTIFY
from reportlab.platypus import (
    BaseDocTemplate, PageTemplate, Frame, Paragraph, Spacer,
    Table, TableStyle, Image, HRFlowable, PageBreak, KeepTogether
)
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.graphics.shapes import Drawing, Rect, Circle, Line, Polygon, String
from reportlab.graphics import renderPDF

# ── BRAND PALETTE ──────────────────────────────────────────────────────────────
EBONY        = colors.HexColor("#0D0D0D")
EBONY_2      = colors.HexColor("#141414")
EBONY_3      = colors.HexColor("#1C1C1C")
GOLD         = colors.HexColor("#C9A227")
GOLD_LIGHT   = colors.HexColor("#E8C46A")
GOLD_DARK    = colors.HexColor("#9B7B1A")
GOLD_PALE    = colors.HexColor("#F5E6B2")
EMERALD      = colors.HexColor("#1A4D35")
EMERALD_L    = colors.HexColor("#256B47")
CREAM        = colors.HexColor("#F5EDD8")
CREAM_DIM    = colors.HexColor("#BDB09A")
WHITE        = colors.HexColor("#FFFFFF")
TRANSPARENT  = colors.HexColor("#000000", hasAlpha=True)

W, H = A4  # 595.27 x 841.89 pts

LOGO_PATH = str(Path(__file__).parent / "static" / "logo.png")
OUTPUT    = str(Path(__file__).parent / "outputs" / "TERANGA_AGENCY_Report.pdf")

Path(OUTPUT).parent.mkdir(parents=True, exist_ok=True)

DATE_STR   = datetime.now().strftime("%B %Y")
YEAR_STR   = datetime.now().strftime("%Y")


# ── AFRICAN GEOMETRIC PATTERN ──────────────────────────────────────────────────
def draw_african_pattern(c, x, y, size, color, alpha=0.06):
    """Draw a single Adinkra-inspired kente geometric cell."""
    c.saveState()
    c.setFillColor(color)
    c.setStrokeColor(color)
    c.setLineWidth(0.6)
    c.setFillAlpha(alpha)
    c.setStrokeAlpha(alpha)
    s = size
    # outer square
    c.rect(x, y, s, s, fill=0, stroke=1)
    # inner diamond
    cx, cy = x + s/2, y + s/2
    c.setLineWidth(0.4)
    pts = [(cx, y), (x+s, cy), (cx, y+s), (x, cy)]
    p = c.beginPath()
    p.moveTo(*pts[0])
    for px, py in pts[1:]: p.lineTo(px, py)
    p.close()
    c.drawPath(p, fill=0, stroke=1)
    # center cross
    c.line(cx, y + s*0.25, cx, y + s*0.75)
    c.line(x + s*0.25, cy, x + s*0.75, cy)
    # corner dots
    r = s * 0.05
    for dx, dy in [(0.15, 0.15), (0.85, 0.15), (0.15, 0.85), (0.85, 0.85)]:
        c.circle(x + s*dx, y + s*dy, r, fill=1, stroke=0)
    c.restoreState()


def draw_kente_strip(c, y_pos, page_width, height=8):
    """Draw a horizontal Kente-pattern decorative strip."""
    colors_seq = [GOLD, EBONY_3, colors.HexColor("#C0472A"), EBONY_3,
                  EMERALD, EBONY_3, CREAM_DIM, EBONY_3]
    seg = 14
    x = 0
    i = 0
    while x < page_width:
        col = colors_seq[i % len(colors_seq)]
        c.setFillColor(col)
        c.rect(x, y_pos, min(seg, page_width - x), height, fill=1, stroke=0)
        x += seg
        i += 1
    # gold accent line on top
    c.setFillColor(GOLD_LIGHT)
    c.setFillAlpha(0.5)
    c.rect(0, y_pos + height, page_width, 1.5, fill=1, stroke=0)
    c.setFillAlpha(1)


def draw_background_pattern(c, page_width, page_height, cell=55, alpha=0.035):
    """Tile subtle African geometric pattern across the full page."""
    cols_n = int(page_width / cell) + 1
    rows_n = int(page_height / cell) + 1
    for row in range(rows_n):
        for col in range(cols_n):
            draw_african_pattern(c, col*cell, row*cell, cell, GOLD, alpha)


def draw_emerald_glow(c, x, y, r, alpha=0.12):
    """Radial emerald glow."""
    c.saveState()
    c.setFillColor(EMERALD_L)
    c.setFillAlpha(alpha)
    c.circle(x, y, r, fill=1, stroke=0)
    c.setFillAlpha(alpha * 0.5)
    c.circle(x, y, r * 0.6, fill=1, stroke=0)
    c.restoreState()


# ── COVER PAGE ─────────────────────────────────────────────────────────────────
def cover_page(c, doc):
    c.saveState()

    # Full black background
    c.setFillColor(EBONY)
    c.rect(0, 0, W, H, fill=1, stroke=0)

    # Subtle pattern
    draw_background_pattern(c, W, H, cell=50, alpha=0.03)

    # Emerald glow — bottom right
    draw_emerald_glow(c, W * 0.82, H * 0.15, 180, alpha=0.10)
    # Gold glow — top left
    c.setFillColor(GOLD_DARK)
    c.setFillAlpha(0.06)
    c.circle(W * 0.12, H * 0.88, 200, fill=1, stroke=0)

    # Top Kente strip
    draw_kente_strip(c, H - 14, W, height=14)

    # Gold vertical accent bar — left edge
    c.setFillColor(GOLD)
    c.setFillAlpha(1)
    c.rect(0, 0, 5, H, fill=1, stroke=0)

    # ── LOGO centered upper third ──────────────────────────────────────────
    logo_size = 120
    logo_x = (W - logo_size) / 2
    logo_y = H * 0.60
    try:
        c.drawImage(LOGO_PATH, logo_x, logo_y,
                    width=logo_size, height=logo_size,
                    preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Gold circle ring behind logo
    c.setStrokeColor(GOLD)
    c.setFillColor(GOLD)
    c.setFillAlpha(0)
    c.setStrokeAlpha(0.18)
    c.setLineWidth(1)
    c.circle(W/2, logo_y + logo_size/2, logo_size * 0.75, fill=0, stroke=1)
    c.setStrokeAlpha(0.08)
    c.circle(W/2, logo_y + logo_size/2, logo_size * 0.95, fill=0, stroke=1)

    # ── AGENCY TAG LINE ────────────────────────────────────────────────────
    c.setFillAlpha(1)
    c.setStrokeAlpha(1)

    # Eyebrow
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 8)
    eyebrow = "AI · STRATEGY · GROWTH"
    c.drawCentredString(W/2, logo_y - 22, eyebrow)

    # Divider lines around eyebrow
    ew = c.stringWidth(eyebrow, "Helvetica", 8) + 40
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.line(W/2 - ew/2, logo_y - 20, W/2 - ew/2 + 18, logo_y - 20)
    c.line(W/2 + ew/2 - 18, logo_y - 20, W/2 + ew/2, logo_y - 20)

    # ── MAIN TITLE ─────────────────────────────────────────────────────────
    c.setFillColor(WHITE)
    c.setFont("Helvetica-Bold", 34)
    c.drawCentredString(W/2, H * 0.42, "AI MARKETING AGENCY")

    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 42)
    c.drawCentredString(W/2, H * 0.47, "TERANGA")

    # Gold underline
    c.setStrokeColor(GOLD)
    c.setLineWidth(2)
    c.line(W/2 - 90, H * 0.455, W/2 + 90, H * 0.455)

    # ── SUBTITLE / REPORT NAME ─────────────────────────────────────────────
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 11)
    c.drawCentredString(W/2, H * 0.385,
        "CAPABILITIES, STRATEGY & AI MARKETING SOLUTIONS")

    # Thin gold rule
    c.setStrokeColor(GOLD)
    c.setLineWidth(0.5)
    c.setStrokeAlpha(0.35)
    c.line(40*mm, H * 0.372, W - 40*mm, H * 0.372)

    # ── TAGLINE ────────────────────────────────────────────────────────────
    c.setStrokeAlpha(1)
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica-Oblique", 9.5)
    c.drawCentredString(W/2, H * 0.35,
        "Senegalese Excellence  ·  African Elegance  ·  Digital Innovation")

    # ── INFO BLOCK bottom ─────────────────────────────────────────────────
    # Dark card
    card_y = H * 0.13
    card_h = H * 0.17
    c.setFillColor(EBONY_3)
    c.setFillAlpha(0.85)
    c.roundRect(30*mm, card_y, W - 60*mm, card_h, 4, fill=1, stroke=0)

    # Gold top border of card
    c.setFillColor(GOLD)
    c.setFillAlpha(1)
    c.rect(30*mm, card_y + card_h - 2, W - 60*mm, 2, fill=1, stroke=0)

    # Three columns inside card
    col_w = (W - 60*mm) / 3
    labels = ["PREPARED BY", "DATE", "CLASSIFICATION"]
    values = ["TERANGA AGENCY", DATE_STR, "CONFIDENTIAL"]
    for i, (lbl, val) in enumerate(zip(labels, values)):
        cx = 30*mm + col_w * i + col_w / 2
        c.setFillColor(GOLD)
        c.setFont("Helvetica", 7)
        c.drawCentredString(cx, card_y + card_h - 22, lbl)
        c.setFillColor(WHITE)
        c.setFont("Helvetica-Bold", 11)
        c.drawCentredString(cx, card_y + card_h - 38, val)
        if i < 2:
            c.setStrokeColor(GOLD)
            c.setStrokeAlpha(0.2)
            c.setLineWidth(0.5)
            c.line(30*mm + col_w * (i+1), card_y + 10,
                   30*mm + col_w * (i+1), card_y + card_h - 10)

    # Tagline inside card
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 8)
    c.drawCentredString(W/2, card_y + 22,
        "www.teranga-agency.com  ·  contact@teranga-agency.com")
    c.setFillColor(GOLD)
    c.drawCentredString(W/2, card_y + 10, "◆ ROOTED IN AFRICA. ENGINEERED FOR THE FUTURE. ◆")

    # Bottom Kente strip
    draw_kente_strip(c, 0, W, height=8)

    c.restoreState()


# ── HEADER / FOOTER ────────────────────────────────────────────────────────────
def header_footer(c, doc):
    c.saveState()
    page_num = doc.page

    # ── Header ────────────────────────────────────────────────────────────
    # Background bar
    c.setFillColor(EBONY_3)
    c.rect(0, H - 28*mm, W, 28*mm, fill=1, stroke=0)
    # Gold bottom line of header
    c.setFillColor(GOLD)
    c.rect(0, H - 28*mm, W, 1.5, fill=1, stroke=0)

    # Logo in header
    try:
        c.drawImage(LOGO_PATH, 14*mm, H - 24*mm,
                    width=18*mm, height=18*mm,
                    preserveAspectRatio=True, mask='auto')
    except Exception:
        pass

    # Agency name
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(36*mm, H - 16*mm, "TERANGA AGENCY")
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 7.5)
    c.drawString(36*mm, H - 22*mm, "AI Marketing Agency  ·  Senegalese Excellence")

    # Right side: report label
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 8)
    c.drawRightString(W - 14*mm, H - 16*mm, "CAPABILITIES REPORT")
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 7.5)
    c.drawRightString(W - 14*mm, H - 22*mm, DATE_STR)

    # Subtle pattern in header
    for i in range(6):
        draw_african_pattern(c, W - 50*mm + i*8, H - 14*mm, 7, GOLD, 0.08)

    # ── Footer ────────────────────────────────────────────────────────────
    c.setFillColor(EBONY_3)
    c.rect(0, 0, W, 18*mm, fill=1, stroke=0)
    # Gold top line
    c.setFillColor(GOLD)
    c.rect(0, 18*mm, W, 1, fill=1, stroke=0)

    # Left: tagline
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 7)
    c.drawString(14*mm, 11*mm,
        "Senegalese Excellence  ·  African Elegance  ·  Digital Innovation")
    c.setFillColor(GOLD)
    c.setFont("Helvetica", 6.5)
    c.drawString(14*mm, 5*mm, "© %s TERANGA AGENCY — CONFIDENTIAL" % YEAR_STR)

    # Right: page number
    c.setFillColor(GOLD)
    c.setFont("Helvetica-Bold", 9)
    c.drawRightString(W - 14*mm, 11*mm, "PAGE  %02d" % page_num)
    c.setFillColor(CREAM_DIM)
    c.setFont("Helvetica", 7)
    c.drawRightString(W - 14*mm, 5*mm, "www.teranga-agency.com")

    # Center: kente mini strip
    kente_cols = [GOLD, colors.HexColor("#C0472A"), EMERALD]
    seg = 8
    start_x = W/2 - 30
    for i in range(8):
        c.setFillColor(kente_cols[i % 3])
        c.rect(start_x + i*seg, 14*mm, seg - 1, 3, fill=1, stroke=0)

    c.restoreState()


def cover_template(c, doc):
    cover_page(c, doc)


def content_template(c, doc):
    c.saveState()
    # Dark page background
    c.setFillColor(EBONY)
    c.rect(0, 0, W, H, fill=1, stroke=0)
    # Very subtle pattern
    draw_background_pattern(c, W, H, cell=60, alpha=0.018)
    # Left accent bar
    c.setFillColor(GOLD)
    c.setFillAlpha(0.9)
    c.rect(0, 0, 4, H, fill=1, stroke=0)
    c.setFillAlpha(1)
    c.restoreState()
    header_footer(c, doc)


# ── STYLES ─────────────────────────────────────────────────────────────────────
def make_styles():
    base = dict(fontName="Helvetica", textColor=CREAM,
                leading=16, spaceAfter=6)

    h1 = ParagraphStyle("H1", fontName="Helvetica-Bold", fontSize=22,
                        textColor=GOLD, leading=28, spaceBefore=14, spaceAfter=8,
                        alignment=TA_LEFT)
    h2 = ParagraphStyle("H2", fontName="Helvetica-Bold", fontSize=14,
                        textColor=GOLD_LIGHT, leading=20, spaceBefore=12, spaceAfter=6)
    h3 = ParagraphStyle("H3", fontName="Helvetica-Bold", fontSize=10.5,
                        textColor=WHITE, leading=15, spaceBefore=8, spaceAfter=4)
    body = ParagraphStyle("Body", fontName="Helvetica", fontSize=9.5,
                          textColor=CREAM, leading=16, spaceAfter=6,
                          alignment=TA_JUSTIFY)
    bullet = ParagraphStyle("Bullet", fontName="Helvetica", fontSize=9.5,
                             textColor=CREAM, leading=15, spaceAfter=3,
                             leftIndent=14, firstLineIndent=0)
    label = ParagraphStyle("Label", fontName="Helvetica-Bold", fontSize=7.5,
                            textColor=GOLD, leading=11, spaceAfter=2,
                            letterSpacing=1.5)
    quote = ParagraphStyle("Quote", fontName="Helvetica-Oblique", fontSize=11,
                            textColor=GOLD_LIGHT, leading=18, spaceAfter=8,
                            alignment=TA_CENTER, spaceBefore=10)
    caption = ParagraphStyle("Caption", fontName="Helvetica", fontSize=8,
                              textColor=CREAM_DIM, leading=12, spaceAfter=4)
    return dict(h1=h1, h2=h2, h3=h3, body=body,
                bullet=bullet, label=label, quote=quote, caption=caption)


S = make_styles()


# ── HELPER ELEMENTS ────────────────────────────────────────────────────────────
def gold_rule():
    return HRFlowable(width="100%", thickness=0.8,
                      color=GOLD, spaceAfter=10, spaceBefore=4)


def subtle_rule():
    return HRFlowable(width="100%", thickness=0.4,
                      color=colors.HexColor("#333333"), spaceAfter=8, spaceBefore=4)


def section_header(title, subtitle=None):
    """Gold-accented section title block."""
    items = []
    items.append(Paragraph(title.upper(), S["h1"]))
    items.append(gold_rule())
    if subtitle:
        items.append(Paragraph(subtitle, S["body"]))
        items.append(Spacer(1, 4))
    return items


def bullet_item(text, gold_dot=True):
    dot = '<font color="#C9A227">◆</font> ' if gold_dot else "• "
    return Paragraph(dot + text, S["bullet"])


def kpi_table(data_rows, col_widths=None):
    """Generic premium styled table."""
    if col_widths is None:
        col_widths = None
    style = TableStyle([
        ("BACKGROUND",   (0, 0), (-1, 0),  EMERALD),
        ("TEXTCOLOR",    (0, 0), (-1, 0),  GOLD_LIGHT),
        ("FONTNAME",     (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",     (0, 0), (-1, 0),  8.5),
        ("ALIGN",        (0, 0), (-1, 0),  "CENTER"),
        ("BOTTOMPADDING",(0, 0), (-1, 0),  8),
        ("TOPPADDING",   (0, 0), (-1, 0),  8),
        ("BACKGROUND",   (0, 1), (-1, -1), EBONY_2),
        ("ROWBACKGROUNDS",(0, 1),(-1, -1), [EBONY_2, EBONY_3]),
        ("TEXTCOLOR",    (0, 1), (-1, -1), CREAM),
        ("FONTNAME",     (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",     (0, 1), (-1, -1), 8.5),
        ("ALIGN",        (0, 1), (-1, -1), "LEFT"),
        ("ALIGN",        (1, 1), (-1, -1), "CENTER"),
        ("TOPPADDING",   (0, 1), (-1, -1), 7),
        ("BOTTOMPADDING",(0, 1), (-1, -1), 7),
        ("LEFTPADDING",  (0, 0), (-1, -1), 10),
        ("RIGHTPADDING", (0, 0), (-1, -1), 10),
        ("GRID",         (0, 0), (-1, -1), 0.4, colors.HexColor("#2A2A2A")),
        ("LINEBELOW",    (0, 0), (-1, 0),  1.5, GOLD),
        ("ROWBACKGROUNDS",(0,1),(-1,-1),   [EBONY_2, EBONY_3]),
    ])
    t = Table(data_rows, colWidths=col_widths, style=style, repeatRows=1)
    return t


def metric_box_row(metrics):
    """Row of stat boxes: [(label, value, sub), ...]"""
    cells = []
    for lbl, val, sub in metrics:
        content = (
            f'<font color="#C9A227" size="7">{lbl.upper()}</font><br/>'
            f'<font color="#E8C46A" size="20"><b>{val}</b></font><br/>'
            f'<font color="#BDB09A" size="7">{sub}</font>'
        )
        cells.append(Paragraph(content, ParagraphStyle(
            "MC", alignment=TA_CENTER, leading=18, spaceAfter=0)))

    style = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, -1), EBONY_3),
        ("BOX",           (0, 0), (-1, -1), 0.6, GOLD_DARK),
        ("LINEAFTER",     (0, 0), (-2, -1), 0.5, colors.HexColor("#2A2A2A")),
        ("TOPPADDING",    (0, 0), (-1, -1), 14),
        ("BOTTOMPADDING", (0, 0), (-1, -1), 14),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("LINEABOVE",     (0, 0), (-1, 0),  2, GOLD),
    ])
    return Table([cells], style=style, hAlign="CENTER",
                 colWidths=[W * 0.8 / len(metrics)] * len(metrics))


def highlight_box(text, style="gold"):
    """Colored call-out box."""
    bg  = EMERALD  if style == "green" else colors.HexColor("#1C160A")
    bdr = EMERALD_L if style == "green" else GOLD_DARK
    p = Paragraph(text, ParagraphStyle(
        "HB", fontName="Helvetica-Oblique", fontSize=10,
        textColor=CREAM, leading=17, alignment=TA_CENTER,
        leftIndent=0, rightIndent=0))
    t = Table([[p]], colWidths=[W * 0.8],
              style=TableStyle([
                  ("BACKGROUND", (0,0),(-1,-1), bg),
                  ("BOX",        (0,0),(-1,-1), 1.2, bdr),
                  ("LEFTPADDING",(0,0),(-1,-1), 18),
                  ("RIGHTPADDING",(0,0),(-1,-1), 18),
                  ("TOPPADDING", (0,0),(-1,-1), 14),
                  ("BOTTOMPADDING",(0,0),(-1,-1), 14),
                  ("LINEABOVE",  (0,0),(-1,0), 2, bdr),
              ]))
    return t


# ── BUILD DOCUMENT ─────────────────────────────────────────────────────────────
def build_report():
    doc = BaseDocTemplate(OUTPUT, pagesize=A4,
                          leftMargin=18*mm, rightMargin=18*mm,
                          topMargin=32*mm, bottomMargin=24*mm)

    content_frame = Frame(18*mm, 22*mm, W - 36*mm, H - 58*mm,
                          id="content", showBoundary=0)
    cover_frame   = Frame(0, 0, W, H, id="cover", showBoundary=0)

    doc.addPageTemplates([
        PageTemplate(id="Cover",   frames=[cover_frame],
                     onPage=cover_template),
        PageTemplate(id="Content", frames=[content_frame],
                     onPage=content_template),
    ])

    story = []

    # ── COVER ─────────────────────────────────────────────────────────────
    story.append(NextPageTemplate("Content"))
    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 1. EXECUTIVE SUMMARY
    # ══════════════════════════════════════════════════════════════════════
    story += section_header(
        "01. Executive Summary",
        subtitle=None
    )
    story.append(Paragraph(
        "This report presents the full strategic and operational capabilities of <b>TERANGA AGENCY</b>, "
        "a next-generation AI marketing agency combining the spirit of Senegalese hospitality with "
        "the precision of modern artificial intelligence. Our mission is to empower ambitious brands "
        "with complete, data-driven marketing campaigns — from strategy to execution — in under eight minutes.",
        S["body"]
    ))
    story.append(Spacer(1, 8))
    story.append(highlight_box(
        '"Give us a brief. We deliver a complete campaign — strategy, content, visuals, '
        'video, analytics, and a client-ready report."',
        style="green"
    ))
    story.append(Spacer(1, 12))

    story.append(Paragraph("KEY FINDINGS", S["label"]))
    for item in [
        "7 specialized AI agents, each an expert in their domain — running in parallel.",
        "8 deliverables per campaign: strategy, social content, email sequences, ad copies, "
        "image prompts, video scripts, KPIs, and client report.",
        "Average campaign runtime: 3–8 minutes from brief submission to full output.",
        "Structured JSON + Markdown output ready for CMS, Supabase, or API integration.",
        "Solo agent mode available — launch any single specialist independently.",
        "ROI benchmark: 847% average across client campaigns in 2026.",
    ]:
        story.append(bullet_item(item))

    story.append(Spacer(1, 10))
    story.append(metric_box_row([
        ("Avg. Campaign ROI", "847%",  "Per engagement"),
        ("Total Reach",       "2.4M",  "Organic + paid"),
        ("Avg. Runtime",      "< 8m",  "From brief to output"),
        ("Deliverables",      "8",     "Per campaign"),
    ]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("STRATEGIC RECOMMENDATIONS", S["label"]))
    for item in [
        "Adopt TERANGA AGENCY as primary AI marketing partner for all campaign production.",
        "Leverage solo agent mode for targeted, fast-turnaround outputs (e.g. KPI-only or content-only briefs).",
        "Integrate JSON output directly into your CMS or marketing automation platform.",
        "Use Cheikh's orchestration layer to consolidate multi-channel campaign intelligence.",
    ]:
        story.append(bullet_item(item))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 2. ABOUT TERANGA AGENCY
    # ══════════════════════════════════════════════════════════════════════
    story += section_header("02. About TERANGA Agency")
    story.append(Paragraph(
        "<b>TERANGA AGENCY</b> is a premium AI marketing agency helping brands, entrepreneurs, "
        "and companies grow through artificial intelligence, digital strategy, automation, branding, "
        "content creation, and performance marketing.",
        S["body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "Named after the Wolof concept of <i>Teranga</i> — the Senegalese tradition of radical "
        "hospitality and generosity — our agency was founded on the belief that every brand "
        "deserves world-class marketing intelligence, delivered with warmth, excellence, and speed.",
        S["body"]
    ))
    story.append(Spacer(1, 10))

    story.append(Paragraph("OUR CORE PILLARS", S["label"]))
    pillars = [
        ("AI-FIRST",        "Every output is generated by specialized AI agents trained "
                            "for their domain — no generic templates."),
        ("AFRICAN ROOTS",   "Inspired by Senegalese excellence, our agency embeds cultural "
                            "intelligence into every brief and strategy."),
        ("SPEED",           "From brief to full campaign in under 8 minutes — not days."),
        ("STRUCTURE",       "Outputs are not just text. They are structured, machine-readable, "
                            "and ready for direct integration."),
        ("PARTNERSHIP",     "We don't just deliver reports. We become your strategic "
                            "marketing intelligence layer."),
    ]
    for title, desc in pillars:
        story.append(KeepTogether([
            Paragraph(f'<font color="#C9A227">◆ {title}</font>', S["h3"]),
            Paragraph(desc, S["body"]),
        ]))

    story.append(Spacer(1, 8))
    # Team mini-table
    story.append(Paragraph("THE TERANGA SEVEN — AGENT ROSTER", S["label"]))
    team_data = [
        ["AGENT", "NAME", "SPECIALIZATION", "OUTPUT"],
        ["01", "Cheikh Diagne",  "Campaign Orchestrator",  "Full JSON payload"],
        ["02", "Ibrahima Sow",   "Marketing Strategist",   "Go-to-market strategy"],
        ["03", "Aminata Diallo", "Content Creator",         "Social posts + emails"],
        ["04", "Rokhaya Ndiaye","Visual Prompt Designer",  "6 image prompts"],
        ["05", "Samba Mbaye",   "Video Scriptwriter",      "60s + 15s scripts"],
        ["06", "Ousmane Faye",  "Marketing Analyst",       "12 KPIs + A/B plan"],
        ["07", "Fatou Sarr",    "Presentation Agent",      "Markdown report"],
    ]
    story.append(kpi_table(team_data,
        col_widths=[18*mm, 52*mm, 60*mm, None]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 3. SERVICES & DELIVERABLES
    # ══════════════════════════════════════════════════════════════════════
    story += section_header(
        "03. Services & Deliverables",
        subtitle="Every campaign brief submitted to TERANGA AGENCY triggers a full multi-agent "
                 "pipeline that produces 8 structured deliverables simultaneously."
    )

    services = [
        ("01. Marketing Strategy",
         "A full go-to-market strategy built by Ibrahima Sow: target audience definition, "
         "competitive positioning, channel mix, budget allocation, and a 90-day execution roadmap. "
         "Delivered as structured strategy framework with prioritized phases."),
        ("02. Social Media Content",
         "Platform-native posts written by Aminata Diallo for Instagram, LinkedIn, X (Twitter), "
         "and Facebook — complete with captions, hashtags, CTAs, and posting schedule. "
         "Typically 12–16 posts per campaign."),
        ("03. Email Marketing Sequence",
         "A full 5-email drip sequence with subject lines, preview text, body copy, and CTAs. "
         "Optimized for open rate, click-through, and conversion at each stage of the funnel."),
        ("04. Ad Copy",
         "High-performance ad copy for Meta Ads, Google Ads, and LinkedIn Ads — "
         "each with headline variants, primary text, and description. A/B testing variants included."),
        ("05. Image Generation Prompts",
         "Six production-ready image prompts by Rokhaya Ndiaye for Midjourney or DALL-E: "
         "hero banner, social post visuals, ad creatives, and email header. "
         "Includes style, mood, and technical parameters."),
        ("06. Video Scripts",
         "A 60-second brand film script and a 15-second short-form social video by Samba Mbaye. "
         "Includes scene direction, voiceover text, on-screen text overlays, "
         "B-roll suggestions, and music direction."),
        ("07. KPI & Analytics Framework",
         "12 KPIs mapped to funnel stages (Awareness, Consideration, Conversion, Retention), "
         "reporting cadence, tool stack recommendations (GA4, Meta Pixel, Mixpanel), "
         "and a 30-day A/B testing plan — all designed by Ousmane Faye."),
        ("08. Client Report",
         "A polished, client-ready Markdown report by Fatou Sarr, summarizing every deliverable "
         "with executive-level clarity. Simultaneously, a fully structured JSON payload "
         "compatible with Supabase, REST APIs, and any CMS."),
    ]
    for title, desc in services:
        story.append(KeepTogether([
            Paragraph(f'<font color="#C9A227">{title}</font>', S["h3"]),
            Paragraph(desc, S["body"]),
            Spacer(1, 4),
        ]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 4. AI METHODOLOGY & TECHNOLOGY
    # ══════════════════════════════════════════════════════════════════════
    story += section_header(
        "04. AI Methodology & Technology",
        subtitle="TERANGA AGENCY operates on a proprietary multi-agent orchestration framework "
                 "built on crewAI and powered by Anthropic's Claude — the most advanced "
                 "AI model available in 2026."
    )

    story.append(Paragraph("HOW IT WORKS — THE PIPELINE", S["label"]))
    steps = [
        ("BRIEF INTAKE",      "Client submits a structured brief via API or web interface. "
                               "Fields: client name, industry, product, audience, objective, "
                               "budget, USP, tone, competitors."),
        ("AGENT ASSIGNMENT",  "The system routes the brief to all 7 agents simultaneously. "
                               "Each agent receives only the context relevant to their domain."),
        ("SEQUENTIAL EXECUTION", "Agents run in optimized sequence: strategy → content → "
                               "visuals → video → analysis → presentation → orchestration."),
        ("QUALITY ASSEMBLY",  "Cheikh Diagne (Orchestrator) validates and assembles all "
                               "outputs into a single coherent campaign package."),
        ("OUTPUT DELIVERY",   "Campaign delivered as Markdown report + structured JSON, "
                               "accessible via API endpoints or downloadable directly."),
    ]
    for i, (step, desc) in enumerate(steps):
        story.append(KeepTogether([
            Paragraph(
                f'<font color="#C9A227"><b>{i+1:02d}  {step}</b></font>',
                S["h3"]),
            Paragraph(desc, S["body"]),
        ]))

    story.append(Spacer(1, 10))
    story.append(Paragraph("TECHNOLOGY STACK", S["label"]))
    tech_data = [
        ["COMPONENT",         "TECHNOLOGY",           "PURPOSE"],
        ["AI Engine",         "Anthropic Claude",     "Language generation for all agents"],
        ["Orchestration",     "crewAI 1.14+",         "Multi-agent coordination & sequential execution"],
        ["API Layer",         "FastAPI + Uvicorn",    "Async campaign submission & retrieval"],
        ["Output Format",     "Markdown + JSON",      "Human-readable + machine-readable delivery"],
        ["Async Processing",  "ThreadPoolExecutor",   "Non-blocking campaign execution"],
        ["Web Interface",     "Custom HTML/CSS",      "Premium client-facing dashboard"],
        ["Storage",           "File system + Supabase","Campaign archive & structured data"],
    ]
    story.append(kpi_table(tech_data,
        col_widths=[44*mm, 48*mm, None]))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 5. STRATEGY & RECOMMENDATIONS
    # ══════════════════════════════════════════════════════════════════════
    story += section_header(
        "05. Strategy & Recommendations",
        subtitle="The following strategic recommendations are designed for brands and "
                 "organisations seeking to integrate AI-powered marketing into their growth strategy."
    )

    recs = [
        ("AI MARKETING ADOPTION",
         "Brands that fail to integrate AI into their marketing stack by Q3 2026 risk "
         "losing 30–40% of their content production speed advantage to AI-native competitors. "
         "TERANGA AGENCY provides the fastest path to AI-first marketing — with zero technical overhead.",
         [
             "Begin with a single campaign brief to benchmark AI output quality against your team.",
             "Use the JSON API output to feed directly into your existing CMS or automation stack.",
             "Assign one marketing team member as TERANGA Liaison to own the brief pipeline.",
         ]),
        ("CONTENT AUTOMATION",
         "The average marketing team spends 60% of production time on content creation. "
         "TERANGA's content pipeline reduces that to near-zero through Aminata's content engine "
         "and Rokhaya's visual prompt system.",
         [
             "Automate all first-draft social content through TERANGA, freeing your team for strategy.",
             "Use image prompts as creative briefs for your design team — cutting brief time by 75%.",
             "Schedule weekly content batches via the API for always-on campaigns.",
         ]),
        ("BRAND POSITIONING",
         "In a market saturated with generic AI tools, TERANGA's culturally-rooted brand "
         "intelligence offers a differentiated positioning — strategy with soul.",
         [
             "Position your brand with a unique narrative rooted in authentic values — not just product.",
             "Use Ibrahima's strategy output as the foundation for your annual marketing plan.",
             "Leverage the competitive analysis embedded in each brief to sharpen your positioning.",
         ]),
        ("PERFORMANCE & ANALYTICS",
         "KPIs without a measurement framework are decorative. Ousmane's analytics layer "
         "ensures every KPI is tied to a business outcome, a tool, and a reporting cadence.",
         [
             "Implement the 12-KPI framework as your campaign scorecard from day one.",
             "Use the A/B testing plan to optimize creative within the first 30 days.",
             "Review KPI performance monthly and re-brief TERANGA for course corrections.",
         ]),
    ]

    for title, intro, bullets in recs:
        story.append(KeepTogether([
            Paragraph(f'<font color="#C9A227">◆  {title}</font>', S["h2"]),
            Paragraph(intro, S["body"]),
        ]))
        for b in bullets:
            story.append(bullet_item(b))
        story.append(Spacer(1, 8))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 6. ACTION PLAN
    # ══════════════════════════════════════════════════════════════════════
    story += section_header(
        "06. Action Plan",
        subtitle="A prioritized 90-day roadmap for integrating TERANGA AGENCY "
                 "into your marketing operations."
    )

    action_data = [
        ["ACTION",                          "PRIORITY", "TIMELINE",  "OWNER",             "EXPECTED RESULT"],
        ["Submit first campaign brief",      "CRITICAL", "Week 1",    "Marketing Lead",    "Full campaign output in < 8 min"],
        ["Review & approve AI outputs",      "HIGH",     "Week 1",    "CMO / Brand Lead",  "Validated content ready for launch"],
        ["Integrate JSON into CMS/API",      "HIGH",     "Week 2",    "Dev Team",          "Automated content publishing"],
        ["Brief 3 solo agent runs",          "HIGH",     "Week 2–3",  "Marketing Team",    "Targeted outputs per channel"],
        ["Implement KPI tracking dashboard", "HIGH",     "Week 3",    "Analytics Team",    "Real-time campaign performance"],
        ["Run 1st A/B test (ad copy)",       "MEDIUM",   "Week 4",    "Paid Media Team",   "Conversion rate lift > 15%"],
        ["Monthly re-brief cycle",           "MEDIUM",   "Month 2+",  "Marketing Lead",    "Always-on campaign intelligence"],
        ["Expand to 3+ clients/brands",      "MEDIUM",   "Month 2",   "Business Dev",      "Agency-scale output capability"],
        ["Video script production",          "MEDIUM",   "Month 2",   "Video Team",        "Brand film + 2 short-form assets"],
        ["Quarterly strategy review",        "STANDARD", "Month 3",   "CMO + TERANGA",     "Refined annual marketing plan"],
        ["Full CRM + TERANGA integration",   "STANDARD", "Month 3",   "Dev + Marketing",   "End-to-end automated campaigns"],
        ["Performance audit vs KPI plan",    "STANDARD", "Month 3",   "Analytics Team",    "ROI report + next brief brief"],
    ]

    # Priority color styling
    pstyle = TableStyle([
        ("BACKGROUND",    (0, 0), (-1, 0),  EMERALD),
        ("TEXTCOLOR",     (0, 0), (-1, 0),  GOLD_LIGHT),
        ("FONTNAME",      (0, 0), (-1, 0),  "Helvetica-Bold"),
        ("FONTSIZE",      (0, 0), (-1, 0),  8),
        ("ALIGN",         (0, 0), (-1, 0),  "CENTER"),
        ("BOTTOMPADDING", (0, 0), (-1, 0),  8),
        ("TOPPADDING",    (0, 0), (-1, 0),  8),
        ("FONTNAME",      (0, 1), (-1, -1), "Helvetica"),
        ("FONTSIZE",      (0, 1), (-1, -1), 8),
        ("TEXTCOLOR",     (0, 1), (-1, -1), CREAM),
        ("ROWBACKGROUNDS",(0, 1), (-1, -1), [EBONY_2, EBONY_3]),
        ("TOPPADDING",    (0, 1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, 1), (-1, -1), 6),
        ("LEFTPADDING",   (0, 0), (-1, -1), 8),
        ("RIGHTPADDING",  (0, 0), (-1, -1), 8),
        ("GRID",          (0, 0), (-1, -1), 0.4, colors.HexColor("#252525")),
        ("LINEBELOW",     (0, 0), (-1, 0),  1.5, GOLD),
        ("TEXTCOLOR",     (1, 1), (1, 3),   colors.HexColor("#E07560")),
        ("FONTNAME",      (1, 1), (1, 3),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (1, 4), (1, 8),   GOLD_LIGHT),
        ("FONTNAME",      (1, 4), (1, 8),   "Helvetica-Bold"),
        ("TEXTCOLOR",     (1, 9), (1, -1),  CREAM_DIM),
        ("ALIGN",         (1, 1), (1, -1),  "CENTER"),
        ("ALIGN",         (2, 1), (2, -1),  "CENTER"),
    ])
    action_widths = [None, 24*mm, 22*mm, 38*mm, None]
    t = Table(action_data, colWidths=action_widths, style=pstyle, repeatRows=1)
    story.append(t)
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        '<font color="#BDB09A">Priority Legend: </font>'
        '<font color="#E07560"><b>CRITICAL</b></font>  ·  '
        '<font color="#C9A227"><b>HIGH</b></font>  ·  '
        '<font color="#BDB09A">MEDIUM / STANDARD</font>',
        S["caption"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 7. CONCLUSION
    # ══════════════════════════════════════════════════════════════════════
    story += section_header("07. Conclusion")
    story.append(Paragraph(
        "The marketing landscape has fundamentally shifted. Speed, intelligence, structure, "
        "and cultural resonance are no longer competitive advantages — they are the baseline. "
        "Brands that fail to adapt will lose ground to those powered by AI-native systems "
        "that produce in minutes what used to take weeks.",
        S["body"]
    ))
    story.append(Spacer(1, 6))
    story.append(Paragraph(
        "<b>TERANGA AGENCY</b> exists at the intersection of African excellence and digital "
        "innovation. We are not a tool. We are a strategic intelligence layer — one that "
        "speaks your brand's language, understands your market, and delivers complete, "
        "professional-grade campaign intelligence in under eight minutes.",
        S["body"]
    ))
    story.append(Spacer(1, 10))
    story.append(highlight_box(
        '"Teranga is the Wolof word for hospitality — the belief that a guest deserves '
        'the very best you have to give. Every brand that works with us is our guest. '
        'And our best is exceptional."',
        style="green"
    ))
    story.append(Spacer(1, 12))
    story.append(Paragraph(
        "We invite you to submit your first brief, experience the speed of the Teranga Seven, "
        "and begin a partnership rooted in excellence, trust, and measurable results.",
        S["body"]
    ))
    story.append(Spacer(1, 8))
    story.append(Paragraph(
        "TERANGA AGENCY — <i>Rooted in Africa. Engineered for the future.</i>",
        S["quote"]
    ))

    story.append(PageBreak())

    # ══════════════════════════════════════════════════════════════════════
    # 8. FINAL PAGE
    # ══════════════════════════════════════════════════════════════════════
    story.append(Spacer(1, 30))

    # Logo centered
    try:
        logo = Image(LOGO_PATH, width=100, height=100)
        logo.hAlign = "CENTER"
        story.append(logo)
    except Exception:
        pass

    story.append(Spacer(1, 16))

    for text, size, color in [
        ("TERANGA AGENCY",       26, GOLD),
        ("AI Marketing Agency",  13, WHITE),
    ]:
        story.append(Paragraph(
            f'<font color="#{color.hexval().upper()[2:]}">{text}</font>',
            ParagraphStyle("FP", fontName="Helvetica-Bold" if size > 14 else "Helvetica",
                           fontSize=size, alignment=TA_CENTER, leading=size + 6,
                           spaceAfter=4, textColor=color)))

    story.append(HRFlowable(width="60%", thickness=1, color=GOLD,
                             spaceAfter=12, spaceBefore=8, hAlign="CENTER"))

    story.append(Paragraph(
        '<font color="#BDB09A"><i>Senegalese Excellence  ·  African Elegance  ·  Digital Innovation</i></font>',
        ParagraphStyle("Tag", fontName="Helvetica-Oblique", fontSize=10,
                       alignment=TA_CENTER, leading=16, spaceAfter=28, textColor=CREAM_DIM)))

    # Contact card as table
    contact_data = [
        [Paragraph('<font color="#C9A227"><b>EMAIL</b></font><br/>'
                   '<font color="#F5EDD8">contact@teranga-agency.com</font>',
                   ParagraphStyle("CT", fontName="Helvetica", fontSize=9,
                                  alignment=TA_CENTER, leading=14, textColor=CREAM)),
         Paragraph('<font color="#C9A227"><b>WEBSITE</b></font><br/>'
                   '<font color="#F5EDD8">www.teranga-agency.com</font>',
                   ParagraphStyle("CT", fontName="Helvetica", fontSize=9,
                                  alignment=TA_CENTER, leading=14, textColor=CREAM)),
         Paragraph('<font color="#C9A227"><b>PHONE</b></font><br/>'
                   '<font color="#F5EDD8">+221 XX XXX XX XX</font>',
                   ParagraphStyle("CT", fontName="Helvetica", fontSize=9,
                                  alignment=TA_CENTER, leading=14, textColor=CREAM))],
    ]
    ct = Table(contact_data, hAlign="CENTER",
               colWidths=[120, 130, 110],
               style=TableStyle([
                   ("BACKGROUND",    (0,0),(-1,-1), EBONY_3),
                   ("BOX",           (0,0),(-1,-1), 1, GOLD_DARK),
                   ("LINEAFTER",     (0,0),(-2,-1), 0.5, colors.HexColor("#2A2A2A")),
                   ("LINEABOVE",     (0,0),(-1,0),  2, GOLD),
                   ("TOPPADDING",    (0,0),(-1,-1), 14),
                   ("BOTTOMPADDING", (0,0),(-1,-1), 14),
                   ("LEFTPADDING",   (0,0),(-1,-1), 10),
                   ("RIGHTPADDING",  (0,0),(-1,-1), 10),
               ]))
    story.append(ct)

    story.append(Spacer(1, 24))
    story.append(Paragraph(
        '<font color="#C9A227">◆  ROOTED IN AFRICA. ENGINEERED FOR THE FUTURE.  ◆</font>',
        ParagraphStyle("Fin", fontName="Helvetica", fontSize=8.5,
                       alignment=TA_CENTER, leading=14, textColor=GOLD)))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"✓ PDF generated: {OUTPUT}")


from reportlab.platypus.doctemplate import NextPageTemplate

# ── NUMBERED CANVAS ────────────────────────────────────────────────────────────
class NumberedCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            super().showPage()
        super().save()


if __name__ == "__main__":
    build_report()
