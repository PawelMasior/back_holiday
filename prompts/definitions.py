def prompt_start(name_city: str, 
                desc_user: str,
                date_fr: str,
                date_to: str) -> str:
    return f"""
    Collect basic information about {name_city}

    Requirents:
    - Provide general information about {name_city}.
    - Provide overall fit for turist focused on {desc_user}.

    Save the report in a clear and organized manner.
    """

def prompt_food(name_city: str, 
                desc_user: str) -> str:   
    return f"""
    Please provide a curated list of restaurants in {name_city} tailored for tourists.
    The focus on: {desc_user}.
    
    Requirements:
    - Ensure that the restaurants are currently open.
    - Indicate whether reservations are required.
    - Include the type of cuisine each restaurant offers.
    - Provide the average price range.
    - Mention the address and contact information.
    - Highlight any unique features or specialties.
    
    Save the report in a clear and organized manner.
    """
    
def prompt_events(name_city: str,  
                  desc_user: str, 
                  date_fr: str, 
                  date_to: str) -> str:
    return f"""
    Collect information on events between {date_fr} and {date_to} in {name_city}.
    Focus on {desc_user}.
    
    Requirents:
    - Ensure that the events are scheduled and active between {date_fr} and {date_to}.
    - Indicate whether reservations are required for each event.
    - Include the category of each event (e.g., music, art, sports).
    - Provide the location and venue details.
    - Mention the start and end times of the events.
    - Include any associated costs or ticket prices.
    - Highlight any unique features or special guests.
    - Provide links to event websites for more information.

    Save the report in a clear and organized manner.
    """

# museums
# trips outside
# accomodation

def prompt_final(name_city: str,  
                desc_user: str, 
                date_fr: str, 
                date_to: str,
                bool_restaurants: bool,
                bool_events: bool) -> str:
    prompt =  f"""
        Create a markdown format travel info to {name_city} between {date_fr} and {date_to} based on collected information. 
        
        Requirements:
        - Provide general info about {name_city}.
        - Provide overall fit for turist focused on {desc_user}.
        - Focus only on collected information.
        """
    if bool_restaurants: 
        prompt += f"""
        - Restaurants with information on:
            reservation requirement, opening hours, cousine, specialities, price range, address.
        """
    if bool_events: 
        prompt += f"""
        - Events in {name_city} between {date_fr} and {date_to} with information on:
            reservation requirement, category, time, specialities, unique features, links.
        """    
    return prompt