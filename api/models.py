from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

# Valid solo agent keys
AGENT_KEYS = [
    "strategist",
    "content_creator",
    "visual_designer",
    "video_writer",
    "analyst",
    "presenter",
    "orchestrator",
]


class BriefRequest(BaseModel):
    client_name:                str
    industry:                   str
    product_service:            str
    target_audience:            str
    campaign_objective:         str
    budget:                     Optional[str] = None
    timeline:                   Optional[str] = None
    unique_selling_proposition: str
    competitors:                Optional[str] = None
    tone_of_voice:              Optional[str] = None
    additional_notes:           Optional[str] = None
    # Leave empty for full campaign; set to e.g. ["analyst"] for solo run
    selected_agents:            Optional[List[str]] = None

    model_config = {
        "json_schema_extra": {
            "example": {
                "client_name": "EcoWear",
                "industry": "Sustainable Fashion",
                "product_service": "Activewear made from recycled ocean plastic",
                "target_audience": "Millennials and Gen Z aged 22-38 who care about sustainability",
                "campaign_objective": "500 pre-orders in 30 days, grow Instagram to 10K followers",
                "budget": "$15,000",
                "timeline": "6 weeks",
                "unique_selling_proposition": "Every product removes 5 bottles from the ocean",
                "competitors": "Patagonia, Allbirds, Girlfriend Collective",
                "tone_of_voice": "Bold, authentic, action-oriented — never preachy",
                "additional_notes": "Brand colors: #1B6CA8, #2D6A4F. Founder is ex-marine biologist.",
            }
        }
    }


class CampaignStatus(BaseModel):
    campaign_id: str
    client_name: str
    status:      str   # "running" | "done" | "error"
    started_at:  str
    finished_at: Optional[str] = None
    output_dir:  Optional[str] = None
    error:       Optional[str] = None


class CampaignSummary(BaseModel):
    campaign_id:   str
    campaign_name: Optional[str]
    client_name:   str
    created_at:    str
    output_dir:    str
    social_posts:  int
    emails:        int
    kpis:          int
