# %reset -f
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List
 
class AttractionDetails(BaseModel):
    name: str = Field(..., description="Attraction name")
    category: str = Field(..., description="Type of attraction (e.g., museum, temple)")
    description: str = Field(..., description="Brief description of the attraction")
    unique_feature: str = Field(..., description="What makes the attraction unique")
    address: str = Field(..., description="Attraction address")
    contact: Optional[str] = Field(..., description="Contact information")
    opening_hours: str = Field(..., description="Opening hours of the attraction (e.g., ['Mon-Fri: 9am-5pm', 'Sat-Sun: 10am-6pm'])")
    ticket_info: str = Field(..., description="Ticket purchase and pricing info")
    source: str = Field(..., description="Information source URL")

class Attractions(BaseModel):
    data: List[AttractionDetails] = Field(..., description="Up to top 10 attractions")
    overview: str = Field(..., description="Overview of attractions available in the area")
    sources: str = Field(..., description="Brief describtion on sources used in the research")


    # latitude: Optional[float] = Field(None, description="Latitude of the attraction")
    # longitude: Optional[float] = Field(None, description="Longitude of the attraction")
    # images: Optional[List[HttpUrl]] = Field(None, description="List of image URLs for the attraction")

    # @validator('phone')
    # def validate_phone(cls, v):
    #     if v and not v.startswith('+'):
    #         raise ValueError("Phone number should start with '+' followed by country code")
    #     return v    