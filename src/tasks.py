from crewai import Task
from textwrap import dedent


def _fmt_brief(brief: dict) -> str:
    return "\n".join(
        f"- **{k.replace('_', ' ').title()}**: {v}" for k, v in brief.items()
    )


# ──────────────────────────────────────────────────────────────────
# Shared prompt fragments — injected into every task
# ──────────────────────────────────────────────────────────────────

_RESEARCH_PHASE = dedent("""
    ## Phase 1 — DEEP RESEARCH (mandatory, run BEFORE writing)
    Use your web-search tool to gather real, current evidence about the client's
    market. Target a maximum of 3–5 searches total — be efficient and specific.

    Pull at minimum:
    - **3+ competitor moves in the last 6 months** (launches, campaigns, pricing, positioning)
    - **2+ industry benchmarks with numeric values** (conversion rates, CAC, engagement rates, etc.)
    - **2+ audience insights** (search trends, Reddit/forum discussions, review mining,
      top-performing organic content in this niche)

    For every fact you surface, capture the source as `[source: publication or URL, date]`.
    You will cite these inline in the deliverable.
""").strip()

_QUALITY_BAR = dedent("""
    ## Quality Bar (final review before submitting)
    - Every numeric or market claim carries an inline `[source: …]` citation.
    - Zero generic marketing filler. Every sentence must be specific to THIS client.
    - Zero placeholders. Zero `[INSERT X]`. Zero truncation.
    - If a paragraph could apply to any brand, rewrite it until it could only apply to this one.
    - If you cannot verify a claim, remove it or clearly label it as an assumption.
""").strip()


def create_tasks(agents: dict, brief: dict) -> list[Task]:
    b = _fmt_brief(brief)

    # ──────────────────────────────────────────────────────────────
    # TASK 1 — Marketing Strategy
    # ──────────────────────────────────────────────────────────────
    strategy_task = Task(
        description=dedent(f"""
            Analyze the client brief and produce a comprehensive, actionable, evidence-based
            marketing strategy.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliverable
            Write a structured marketing strategy with these sections:

            1. **Executive Summary** — 3 sentences: situation, strategy, expected outcome.
            2. **Target Audience Analysis** — demographics, psychographics, pain points,
               desires, online behavior (cite audience research sources).
            3. **Competitive Landscape** — where this brand sits vs. named competitors with
               at least one recent move cited per competitor; whitespace opportunities.
            4. **Core Message & Value Proposition** — the single most compelling reason to
               choose this brand, stated in customer language.
            5. **Channel Mix & Rationale** — which channels and why, backed by benchmark data
               (CPM, CTR, conversion rate for this industry — cite sources).
            6. **Campaign Theme & Creative Direction** — the big idea, tagline suggestion,
               visual/tonal direction.
            7. **Budget Allocation** — recommended % breakdown by channel, justified.
            8. **90-Day Roadmap** — three 30-day phases with specific milestones and KPIs.

            Be specific. Use real numbers. Avoid generic marketing advice.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "A detailed, structured marketing strategy document (700–1000 words) covering "
            "all 8 sections with inline `[source: …]` citations on every numeric or market claim."
        ),
        agent=agents["strategist"],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 2 — Content Package
    # ──────────────────────────────────────────────────────────────
    content_task = Task(
        description=dedent(f"""
            Using the marketing strategy above, write all campaign content — fully finished,
            not placeholders. Mine real voice-of-customer language from reviews, forums, and
            trending content in this niche before you write.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliverables

            ### A. Social Media Posts — one per platform, fully written
            For **Instagram**, **LinkedIn**, **X (Twitter)**, and **Facebook**:
            - Full caption (platform-appropriate length and tone)
            - 5–10 relevant hashtags (verify they're not dead — real current tags)
            - CTA
            - Best time to post (day + time, cite benchmark source)

            ### B. Email Sequence — 5 emails, fully written
            | # | Purpose |
            |---|---------|
            | 1 | Welcome / First impression |
            | 2 | Value / Educate |
            | 3 | Story / Social proof |
            | 4 | Offer / Urgency |
            | 5 | Follow-up / Re-engage |

            For each email:
            - Subject line (+ A/B variant)
            - Preview text (max 100 chars)
            - Full body copy (conversational, scannable, uses real voice-of-customer phrases)
            - CTA button text
            - Recommended send day

            ### C. Ad Copy — one per channel, fully written
            For **Google Search**, **Meta (FB/IG)**, and **LinkedIn Ads**:
            - Headline 1 / Headline 2 (respect character limits per platform)
            - Description (respect character limits per platform)
            - CTA button text

            Keep tone consistent with the strategy's creative direction.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Complete content package: 4 social posts, 5 full emails, 3 ad copy sets — all "
            "100% written, platform-native voice, no placeholders, citations where claims are made."
        ),
        agent=agents["content_creator"],
        context=[strategy_task],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 3 — Visual Prompt Design
    # ──────────────────────────────────────────────────────────────
    visual_task = Task(
        description=dedent(f"""
            Using the strategy and content above, write detailed image generation prompts for
            every key asset. First, research current winning visual trends for this niche
            (Behance, Dribbble, Pinterest, top brands in this space).

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliverables: 6 Image Generation Prompts

            | # | Asset | Dimensions |
            |---|-------|------------|
            | 1 | Instagram Feed Post | 1080×1080 |
            | 2 | Instagram Story / Reel Cover | 1080×1920 |
            | 3 | LinkedIn Post Image | 1200×628 |
            | 4 | Facebook / Meta Ad Creative | 1200×628 |
            | 5 | Email Header Image | 600×300 |
            | 6 | Landing Page Hero Banner | 1920×1080 |

            For EACH prompt provide:
            - **Purpose**: what this image is for
            - **Full Prompt**: exhaustive generation prompt — subject, environment, lighting,
              mood, color palette, composition, camera angle, style references, quality
              modifiers (e.g. "8K, photorealistic, golden hour light, shallow depth of field")
            - **Style**: photorealistic / flat design / 3D render / illustration / cinematic
            - **Dimensions**: pixel dimensions
            - **Designer Notes**: variations, references, things to avoid

            Make prompts compatible with both Midjourney v6 and DALL-E 3.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "6 complete, production-ready image generation prompts with full specifications "
            "and designer notes. Each prompt detailed enough to generate without further input."
        ),
        agent=agents["visual_designer"],
        context=[strategy_task, content_task],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 4 — Video Scripts
    # ──────────────────────────────────────────────────────────────
    video_task = Task(
        description=dedent(f"""
            Write two complete video scripts. Before writing, research current top-performing
            video hooks in this niche (TikTok, YouTube Shorts, Reels) and reverse-engineer
            what's working this week.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliverables

            ### Script 1 — 60-Second Brand Video (YouTube / Meta / LinkedIn)
            ### Script 2 — 15-Second Short-Form Video (TikTok / Instagram Reels)

            For EACH script provide:
            - **Title**
            - **Hook** (first 3 seconds — reference the viral hook pattern you're borrowing)
            - **Scene Breakdown** — for every scene:
              - Scene number
              - Duration (e.g. "0:00–0:03")
              - Visual description (camera, shot type, action)
              - Voiceover / Dialogue (exact words, fully written)
              - Text overlay (on-screen caption if any)
            - **CTA** (final 3–5 seconds)
            - **Music / Tone suggestion** (genre, energy level, specific trending track
              references if possible — cite source if you name a trending track)

            Write like a professional screenwriter and director. Zero `[INSERT LINE HERE]`.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Two complete video scripts — one 60-second and one 15-second — with full "
            "scene-by-scene breakdown, exact voiceover text, and music direction. Zero placeholders."
        ),
        agent=agents["video_writer"],
        context=[strategy_task, content_task],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 5 — KPI & Analytics Framework
    # ──────────────────────────────────────────────────────────────
    analytics_task = Task(
        description=dedent(f"""
            Design a complete KPI tracking framework and measurement plan. Every target
            number must be calibrated against a real, cited industry benchmark.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliverables

            ### A. KPI Dashboard — 12 KPIs organized by funnel stage
            Funnel stages: **Awareness → Engagement → Conversion → Retention → Revenue**

            For EACH KPI provide:
            - Metric name
            - Specific numeric target (cite the benchmark source that informed it)
            - Baseline estimate (if available)
            - Exact measurement method (tool + how to pull the number)
            - Reporting frequency (daily / weekly / monthly)

            ### B. Reporting Cadence
            - Weekly check-in: what to review, who attends, format
            - Monthly report: sections, key questions to answer
            - Quarterly business review: strategic adjustments, budget reallocation triggers

            ### C. Recommended Tool Stack
            List 5–6 specific tools (e.g. GA4, Meta Ads Manager, Klaviyo, Hotjar, Amplitude)
            with their role in the stack and approximate monthly cost.

            ### D. 30-Day A/B Testing Plan — 3 specific tests
            Each test: what's tested, hypothesis, success metric, duration, required sample size.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Complete analytics framework: 12 KPIs (each with a cited benchmark source), "
            "reporting cadence, tool stack with costs, and a 3-test A/B plan for the first 30 days."
        ),
        agent=agents["analyst"],
        context=[strategy_task],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 6 — Markdown Report (Presenter — Fatou Sarr)
    # ONLY Markdown. JSON is generated separately in Task 7.
    # ──────────────────────────────────────────────────────────────
    report_task = Task(
        description=dedent(f"""
            Compile all specialist outputs into one polished, client-ready Markdown report.
            Output ONLY Markdown — no JSON in this task.

            Before compiling: verify there are no contradictions between specialists. If
            Ibrahima's target audience conflicts with Aminata's tone, resolve it in your
            "Campaign Coherence Overview" paragraph. Preserve every inline `[source: …]`
            citation from specialists — do not strip them.

            ## Client Brief
            {b}

            ## Report Structure (follow exactly)

            # [Campaign Name] — Full Campaign Package
            **Client:** [Name] | **Date:** [Today] | **Prepared by:** Teranga Agency

            ---

            ## Campaign Coherence Overview
            [1 paragraph connecting all deliverables to strategy and campaign objective.
             Explicitly note how content, visuals, video, and KPIs reinforce the same thesis.]

            ## 1. Marketing Strategy
            [Full strategy from Ibrahima — all 8 sections verbatim, citations preserved]

            ## 2. Content Package
            ### 2.1 Social Media Posts
            [All 4 posts from Aminata — Instagram, LinkedIn, X, Facebook — fully written]
            ### 2.2 Email Sequence
            [All 5 emails from Aminata — fully written, no truncation]
            ### 2.3 Ad Copy
            [All 3 ad sets from Aminata — Google, Meta, LinkedIn]

            ## 3. Visual Assets — Image Generation Prompts
            [All 6 prompts from Rokhaya — fully written]

            ## 4. Video Scripts
            ### 4.1 60-Second Brand Video
            [Full script from Samba]
            ### 4.2 15-Second Short-Form Video
            [Full script from Samba]

            ## 5. KPI & Analytics Framework
            ### 5.1 KPI Dashboard (12 KPIs)
            ### 5.2 Reporting Cadence
            ### 5.3 Tool Stack
            ### 5.4 A/B Testing Plan
            [Full framework from Ousmane]

            ## 6. Next Steps & Timeline
            [5–7 concrete actions with owner and due date]

            ## 7. Sources & References
            [Consolidated bibliography of every `[source: …]` citation that appeared above,
             deduplicated and numbered.]

            ---
            *Prepared by Fatou Sarr — Presentation Lead, Teranga Agency*

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Complete Markdown campaign report — all 7 sections fully written, citations "
            "preserved, sources consolidated at the end. No JSON, no truncation, no placeholders."
        ),
        agent=agents["presenter"],
        context=[strategy_task, content_task, visual_task, video_task, analytics_task],
    )

    # ──────────────────────────────────────────────────────────────
    # TASK 7 — JSON Payload (Orchestrator — Cheikh Diagne)
    # ONLY JSON. No citations inside JSON — citations belong in Markdown.
    # ──────────────────────────────────────────────────────────────
    orchestration_task = Task(
        description=dedent(f"""
            You are Cheikh Diagne, Campaign Orchestrator. Your ONLY job in this task is to
            output a single, valid JSON object — nothing else. No markdown headers, no prose,
            no QA notes. Just the JSON object inside a ```json code block.

            Do NOT include `[source: …]` citations inside JSON strings — those live in
            Fatou's Markdown report only. Keep JSON string values clean for downstream
            Supabase insertion.

            Extract and synthesize data from all previous task outputs to populate this schema:

            ```json
            {{
              "campaign_id": "<generate a uuid-v4>",
              "created_at": "<ISO-8601 datetime for today>",
              "client_name": "{brief.get('client_name', '')}",
              "campaign_name": "<campaign name from the strategy>",
              "strategy": {{
                "overview": "<2-3 sentence summary>",
                "target_audience": "<1-2 sentence description>",
                "positioning": "<1 sentence>",
                "channels": ["<channel1>", "<channel2>"],
                "budget_allocation": {{"<channel>": "<percent>"}},
                "timeline": "<phase summary>"
              }},
              "social_posts": [
                {{
                  "platform": "instagram",
                  "caption": "<full caption — do not truncate>",
                  "hashtags": ["tag1", "tag2"],
                  "cta": "<cta text>",
                  "best_time_to_post": "<day + time>"
                }},
                {{
                  "platform": "linkedin",
                  "caption": "<full caption>",
                  "hashtags": [],
                  "cta": "<cta>",
                  "best_time_to_post": "<day + time>"
                }},
                {{
                  "platform": "x",
                  "caption": "<full post>",
                  "hashtags": [],
                  "cta": "<cta>",
                  "best_time_to_post": "<day + time>"
                }},
                {{
                  "platform": "facebook",
                  "caption": "<full caption>",
                  "hashtags": [],
                  "cta": "<cta>",
                  "best_time_to_post": "<day + time>"
                }}
              ],
              "email_sequence": [
                {{
                  "position": 1,
                  "subject": "<subject>",
                  "preview_text": "<preview>",
                  "body": "<2-3 sentence summary of email body>",
                  "cta": "<cta>",
                  "send_day": "<day>"
                }}
              ],
              "ad_copies": [
                {{
                  "platform": "google",
                  "headline": "<headline>",
                  "description": "<description>",
                  "cta": "<cta>"
                }},
                {{
                  "platform": "meta",
                  "headline": "<headline>",
                  "description": "<description>",
                  "cta": "<cta>"
                }},
                {{
                  "platform": "linkedin",
                  "headline": "<headline>",
                  "description": "<description>",
                  "cta": "<cta>"
                }}
              ],
              "image_prompts": [
                {{
                  "purpose": "<purpose>",
                  "prompt": "<full prompt>",
                  "style": "<style>",
                  "dimensions": "<WxH>",
                  "notes": "<notes>"
                }}
              ],
              "video_scripts": [
                {{
                  "duration": "60s",
                  "title": "<title>",
                  "hook": "<hook line>",
                  "scenes": [
                    {{
                      "scene_number": 1,
                      "timecode": "0:00-0:05",
                      "visual": "<what camera sees>",
                      "voiceover": "<exact words>",
                      "text_overlay": "<on-screen text>"
                    }}
                  ],
                  "cta": "<cta>",
                  "music_direction": "<music note>"
                }},
                {{
                  "duration": "15s",
                  "title": "<title>",
                  "hook": "<hook>",
                  "scenes": [],
                  "cta": "<cta>",
                  "music_direction": "<music>"
                }}
              ],
              "kpis": [
                {{
                  "metric": "<name>",
                  "target": "<number or %>",
                  "baseline": "<baseline>",
                  "measurement_method": "<tool + method>",
                  "frequency": "<daily|weekly|monthly>",
                  "funnel_stage": "<Awareness|Engagement|Conversion|Retention|Revenue>"
                }}
              ],
              "next_steps": [
                {{
                  "action": "<concrete action>",
                  "owner": "<who>",
                  "due_date": "<date>"
                }}
              ]
            }}
            ```

            Rules:
            - Output ONLY the ```json ... ``` block. Nothing before it. Nothing after it.
            - All strings must be valid JSON (escape quotes, no raw line breaks inside strings).
            - Do NOT embed `[source: …]` citations inside string values.
            - email_sequence must have all 5 emails (body can be a 2-3 sentence summary).
            - image_prompts must have all 6 assets.
            - kpis must have at least 8 entries.
            - next_steps must have at least 5 entries.
        """),
        expected_output=(
            "A single valid JSON object inside a ```json code block. Nothing else — "
            "no prose, no headers, no markdown outside the code block, no citation markers."
        ),
        agent=agents["orchestrator"],
        context=[strategy_task, content_task, visual_task, video_task, analytics_task, report_task],
    )

    return [
        strategy_task,
        content_task,
        visual_task,
        video_task,
        analytics_task,
        report_task,
        orchestration_task,
    ]


# ──────────────────────────────────────────────────────────────────
# SOLO TASKS — each agent runs independently with just the brief
# ──────────────────────────────────────────────────────────────────

def create_solo_tasks(agents: dict, brief: dict, selected: list[str]) -> list[Task]:
    """Build standalone tasks for a subset of agents, no interdependencies."""
    b = _fmt_brief({k: v for k, v in brief.items() if k != "selected_agents"})
    tasks = []
    builders = {
        "strategist":      _solo_strategy,
        "content_creator": _solo_content,
        "visual_designer": _solo_visual,
        "video_writer":    _solo_video,
        "analyst":         _solo_analyst,
        "presenter":       _solo_presenter,
        "orchestrator":    _solo_orchestrator,
    }
    for key in selected:
        fn = builders.get(key)
        if fn and key in agents:
            tasks.append(fn(agents[key], b, brief))
    return tasks


def _solo_strategy(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Ibrahima Sow, Senior Marketing Strategist. From the brief below ONLY,
            produce a complete standalone marketing strategy document.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            1. Executive Summary (3 sentences)
            2. Target Audience Analysis (demographics, psychographics, pain points — cite research)
            3. Competitive Landscape & Whitespace (recent competitor moves with sources)
            4. Core Message & Value Proposition
            5. Channel Mix & Rationale (benchmark-backed)
            6. Campaign Theme & Creative Direction
            7. Budget Allocation (% by channel, justified)
            8. 90-Day Phased Roadmap

            Be specific, use real numbers, no filler.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Complete marketing strategy document covering all 8 sections (700–1000 words) "
            "with inline `[source: …]` citations on every numeric/market claim."
        ),
        agent=agent,
    )


def _solo_content(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Aminata Diallo, Senior Content Creator. From the brief below ONLY,
            write all campaign content — fully written, zero placeholders. Mine real
            voice-of-customer language before writing.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            A. Social Media Posts (Instagram, LinkedIn, X, Facebook) — full captions,
               hashtags, CTA, best time to post (cite benchmark source)
            B. Email Sequence (5 emails: Welcome, Value, Story, Offer, Follow-up) —
               full body copy each
            C. Ad Copy (Google Search, Meta, LinkedIn) — headlines + descriptions
               respecting platform character limits

            Platform-native tone throughout. Nothing generic.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "4 social posts + 5 full emails + 3 ad copies — all 100% written, "
            "platform-native, zero placeholders."
        ),
        agent=agent,
    )


def _solo_visual(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Rokhaya Ndiaye, Creative Director & Visual Prompt Engineer.
            From the brief below ONLY, write 6 detailed image generation prompts.
            Research current winning visual trends in this niche before writing.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            One prompt each for:
            1. Instagram Feed (1080×1080)
            2. Instagram Story/Reel Cover (1080×1920)
            3. LinkedIn Post Image (1200×628)
            4. Facebook/Meta Ad Creative (1200×628)
            5. Email Header (600×300)
            6. Landing Page Hero Banner (1920×1080)

            Each prompt: purpose, full generation text (subject, environment, lighting,
            color palette, camera angle, style, quality modifiers), style tag, dimensions,
            notes. Compatible with Midjourney v6 and DALL-E 3.

            {_QUALITY_BAR}
        """),
        expected_output="6 complete image generation prompts, each fully specified.",
        agent=agent,
    )


def _solo_video(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Samba Mbaye, Senior Video Scriptwriter & Director. From the brief below
            ONLY, write two complete video scripts. Research current top-performing video
            hooks in this niche before writing.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            Script 1 — 60-second Brand Video (YouTube/Meta/LinkedIn)
            Script 2 — 15-second Short-Form (TikTok/Reels)

            Each script: title, hook (first 3s, reference the viral pattern borrowed),
            scene-by-scene breakdown (scene #, timecode, visual, voiceover, text overlay),
            CTA, music direction. Every voiceover line fully written. Zero placeholders.

            {_QUALITY_BAR}
        """),
        expected_output="Two complete video scripts — 60s and 15s — with full scene breakdowns.",
        agent=agent,
    )


def _solo_analyst(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Ousmane Faye, Senior Marketing Analyst. From the brief below ONLY,
            design a complete KPI tracking framework. Every target must be calibrated
            against a real, cited industry benchmark.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            A. KPI Dashboard — 12 KPIs across Awareness, Engagement, Conversion, Retention,
               Revenue. Each KPI: metric name, numeric target (with cited benchmark source),
               baseline, measurement method, frequency.
            B. Reporting Cadence — weekly, monthly, quarterly structure.
            C. Tool Stack — 5–6 specific tools with role and approx. monthly cost.
            D. 30-Day A/B Testing Plan — 3 tests with hypothesis, success metric, duration,
               sample size.

            Real numbers. Cited industry benchmarks. No vanity metrics.

            {_QUALITY_BAR}
        """),
        expected_output="12 KPIs + reporting cadence + tool stack + 3-test A/B plan. Fully detailed.",
        agent=agent,
    )


def _solo_presenter(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Fatou Sarr, Senior Presentation Lead. From the brief below ONLY,
            produce a complete executive campaign overview — as if presenting to a client board.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver a polished Markdown document:
            1. Campaign Name & Positioning Statement
            2. Strategic Rationale (why this approach, why now — cite supporting data)
            3. Recommended Channel Mix with budget rationale
            4. Key Messages & Tone Guidance
            5. Success Metrics (5–7 KPIs with targets and benchmark sources)
            6. Proposed Timeline & Milestones
            7. Next Steps (5 concrete actions with owners)
            8. Sources & References (consolidated bibliography)

            Write for a CEO/CMO audience. Clear, precise, no jargon.

            {_QUALITY_BAR}
        """),
        expected_output=(
            "Polished executive campaign overview in Markdown (600–900 words) with a "
            "consolidated Sources & References section."
        ),
        agent=agent,
    )


def _solo_orchestrator(agent, b: str, brief: dict) -> Task:
    return Task(
        description=dedent(f"""
            You are Cheikh Diagne, Campaign Orchestrator & Chief Strategist. From the brief
            below ONLY, produce a high-level campaign master plan — the document that guides
            all other specialists.

            ## Client Brief
            {b}

            {_RESEARCH_PHASE}

            ## Phase 2 — Deliver
            1. Campaign Overview & Core Objective
            2. Team Roles & Responsibilities (who does what, in what order)
            3. Creative Brief (theme, tone, visual direction, key messages)
            4. Channel Priority Stack (ranked by expected ROI, cite benchmarks)
            5. Timeline & Critical Milestones
            6. Risk Assessment (3 risks + mitigation, reference real precedents)
            7. Definition of Success (specific, measurable)

            This is the document every other agent reads before starting. Make it commanding.

            {_QUALITY_BAR}
        """),
        expected_output="Complete campaign master plan document covering all 7 sections.",
        agent=agent,
    )
