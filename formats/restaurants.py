# %reset -f
from pydantic import BaseModel, Field, HttpUrl
from typing import Optional, List

class RestaurantDetails(BaseModel):
    name: str = Field(..., description="Restaurant name")
    cuisine: str = Field(..., description="Main cuisine type")
    price: str = Field(..., description="Average price range with currency")
    unique_feature: str = Field(..., description="What makes the restaurant unique")
    specialty: str = Field(..., description="Signature dish or cuisine specialty")
    phone: str = Field(..., description="Contact phone number")
    address: str = Field(..., description="Restaurant address")
    opening_hours: str = Field(..., description="Opening hours of the restaurant")
    reservation: str = Field(..., description="Reservation requirement info")
    source: HttpUrl = Field(..., description="Information source URL")

class Restaurants(BaseModel):
    data: list[RestaurantDetails] = Field(..., description="Up to top 10 restaurants")
    overview: str = Field(..., description="Overview of restaurants offer in the town")
    summary: str = Field(..., description="Brief summary on sources in completed research")
    