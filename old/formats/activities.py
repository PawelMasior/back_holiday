from pydantic import BaseModel, Field
from typing import Optional, List

class ActivityDetails(BaseModel):
    name: str = Field(..., description="Activity name")
    category: str = Field(..., description="Type of activity (e.g., guided tour, cooking class)")
    description: str = Field(..., description="Brief description of the activity")
    unique_feature: str = Field(..., description="What makes the activity unique")
    location: str = Field(..., description="Location where the activity takes place")
    duration: str = Field(..., description="Duration of the activity")
    age_restrictions: Optional[str] = Field(None, description="Any age restrictions for the activity")
    pricing_info: str = Field(..., description="Pricing information and booking instructions")
    contact: str = Field(..., description="Contact information")
    source: str = Field(..., description="Information source URL")

class Activities(BaseModel):
    data: List[ActivityDetails] = Field(..., description="Up to top 10 activities")
    overview: str = Field(..., description="Overview of activities available in the area")
    sources: str = Field(..., description="Brief describtion on sources used in the research")
