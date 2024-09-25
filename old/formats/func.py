from pydantic import BaseModel, Field
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
    source: str = Field(..., description="Information source URL")

class Restaurants(BaseModel):
    data: list[RestaurantDetails] = Field(..., description="Up to top 10 restaurants")
    overview: str = Field(..., description="Overview of restaurants offer in the town")
    sources: str = Field(..., description="Brief describtion on sources used in the research")


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


class BeyondTheCityDetails(BaseModel):
    name: str = Field(..., description="Activity name or title")
    type: str = Field(..., description="Type of activity (e.g., hiking, castle tour, wine tasting)")
    unique_feature: str = Field(..., description="What makes this activity unique (e.g., scenic view, historical importance)")
    location: str = Field(..., description="Location where the activity takes place (e.g., National Park, beach, castle)")
    duration: str = Field(..., description="The duration of the activity (e.g., 2 hours, full-day)")
    difficulty_level: str = Field(..., description="The difficulty level, if applicable (e.g., easy, moderate, challenging)")
    age_restrictions: Optional[str] = Field(..., description="Age restrictions for the activity, if applicable")
    price: Optional[str] = Field(..., description="Pricing information, including the currency (e.g., $50 USD per person)")
    contact_info: Optional[str] = Field(..., description="Detailed contact information including phone number and website URL")
    source: str = Field(..., description="Information source URL")

class BeyondTheCity(BaseModel):
    data: List[BeyondTheCityDetails] = Field(..., description="A list of up to the top 10 activities beyond the city")
    overview: str = Field(..., description="A summary or overview of the types of activities available beyond the city")
    sources: str = Field(..., description="Brief description of the sources used to collect information")


class FacilityDetails(BaseModel):
    name: str = Field(..., description="Name of the facility or service")
    type: str = Field(..., description="Type of facility or service (e.g., public transport, bike rental, emergency services)")
    unique_feature: str = Field(..., description="What makes this facility or service unique (e.g., 24/7 availability, digital nomad friendly)")
    location: str = Field(..., description="Location or region where the facility/service is available")
    operating_hours: Optional[str] = Field(None, description="Operating hours, if applicable (e.g., 24/7, office hours)")
    price: Optional[str] = Field(None, description="Pricing information, if applicable (e.g., $20 per day for bike rental)")
    contact_info: Optional[str] = Field(None, description="Contact details such as phone number, website URL, or physical address")
    additional_info: Optional[str] = Field(None, description="Additional useful information (e.g., COVID-19 protocols)")
    source: str = Field(..., description="Information source URL")

class Facilities(BaseModel):
    data: List[FacilityDetails] = Field(..., description="A list of up to the top 10 facilities or services available in the city")
    overview: str = Field(..., description="A summary or overview of the types of facilities and services available")
    sources: str = Field(..., description="Brief description of the sources used to collect information")
