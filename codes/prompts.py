

def get_prompt_attractions(query, desc) -> str:
    prompt = f"""
    Provide a curated list of attractions in {query['name_city']} tailored for tourists.
    
    Focus on: {desc}.
    
    Requirements:
    - Specify the type of attraction (e.g., museum, temple).
    - Highlight each attraction's unique feature (e.g., historical significance, artistic value).
    - Include a brief description of each attraction.
    - Provide the location of the attraction.
    - Include the opening hours of the attraction.
    - Include ticket purchase and pricing information (if applicable).
    - Provide detailed contact information: phone number and website URL.
    
    After you collect all data, save the data of the best ones (no duplicates) and finish the task.
    """
    return prompt


def get_prompt_restaurants(query, desc) -> str:  
    prompt = f"""
    Provide a curated list of restaurants in {query['name_city']} tailored for tourists.
    
    Focus on: {desc}.
    
    Requirements:
    - Specify the type of cuisine offered (e.g., Italian, Japanese).
    - Highlight each restaurant's unique feature (e.g., atmosphere, view).
    - Include each restaurant's specialty or signature dish.
    - Include the average price range with currency (e.g., "$$$").
    - Include each restaurant's address.
    - Include the opening hours of the restaurant.
    - Include detailed contact information: phone number and website URL.
    - Clearly indicate whether reservations are required ('Yes', 'No', 'No data').
    
    After you collectcted all data, save the data of the best ones (no duplicates) and finish the task.
    """
    return prompt

def get_prompt_activities(query, desc) -> str:
    prompt = f"""
    Provide a curated list of activities in {query['name_city']} tailored for tourists.
    
    Focus on: {desc}.
    
    Requirements:
    - Specify the type of activity (e.g., guided tours, cooking classes).
    - Highlight each activity's unique feature (e.g., expert guides, local insights).
    - Include a brief description of each activity.
    - Provide the location where the activity takes place.
    - Include the duration of the activity and any age restrictions.
    - Provide pricing information and how to book (e.g., website or phone).
    - Include detailed contact information: phone number and website URL.
    
    After you collect all data, save the data of the best ones (no duplicates) and finish the task.
    """
    return prompt

def get_prompt_beyondthecity(query, desc) -> str:
    prompt = f"""
    Provide a curated list of outdoor and cultural activities beyond the city in {query['name_city']} tailored for tourists.
    
    Focus on: {desc}.
    
    Requirements:
    - Specify the type of activity (e.g., hiking, wine tastings).
    - Highlight each activity's unique feature (e.g., historical importance, scenic landscapes, local expertise).
    - Include a brief but informative description of each activity and its appeal.
    - Provide the specific location or region where the activity takes place (mention proximity to the city, if relevant).
    - Specify the duration of the activity, difficulty level (if applicable), and any age restrictions.
    - Include pricing information and clear instructions on how to book (e.g., website or phone).
    - Provide detailed contact information: phone number and website URL.
    
    After you collect all data, save the data of the best ones (no duplicates) and finish the task.
    """
    return prompt

def get_prompt_facilities(query, desc) -> str:
    prompt = f"""
    Provide a curated list of essential facilities and services available in {query['name_city']} tailored for tourists.
    
    Focus on: {desc}.
    
    Requirements:
    - Specify the type of facility or service (e.g., co-working spaces, public transport options, emergency services).
    - Highlight each facility's or service's unique feature (e.g., 24/7 availability, high-speed internet for digital nomads, accessibility).
    - Include a brief description of each facility or service and what makes it useful or stand out.
    - Provide the location or area where the facility/service is available.
    - Include relevant operating hours and availability (e.g., 24/7, office hours).
    - Provide pricing information (if applicable) and details on how to access the facility/service (e.g., website, phone, physical location).
    - Include contact details: phone number, website URL, or emergency numbers if relevant.
    
    After gathering all data, save most relevant facilities (avoiding duplicates) and complete the task.
    """
    return prompt