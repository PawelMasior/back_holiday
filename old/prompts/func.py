

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


# def prompt_start(query) -> str:
#     prompt = f"""
#     Collect basic information about {query['name_city']}.

#     Requirents:
#     - Provide general information about {query['name_city']}.
#     - Provide overall fit for turist focused on {query['desc_user']}.

#     Save the report in a clear and organized manner.
#     """
#     return prompt
# # print(prompt_start(query))



# def prompt_eating(query) -> str:  
#     prompt = f"""
#     Please provide a curated list of restaurants in {query['name_city']} tailored for tourists.
#     The focus on: {query['desc_user']}.
    
#     Requirements:
#     - Ensure that the restaurants are currently open.
#     - Indicate whether reservations are required.
#     - Include the type of cuisine each restaurant offers.
#     - Provide the average price range.
#     - Mention the address and contact information.
#     - Highlight any unique features or specialties.
    
#     Save the report in a clear and organized manner.
#     """
#     return prompt
# # print(prompt_eating(query))
    
# def prompt_events(query) -> str:
#     prompt = f"""
#     Collect information on events between {query['date_fr']} and {query['date_to']} in {query['name_city']}.
#     Focus on {query['desc_user']}.
    
#     Requirents:
#     - Ensure that the events are scheduled and active between {query['date_fr']} and {query['date_to']}.
#     - Indicate whether reservations are required for each event.
#     - Include the category of each event (e.g., music, art, sports).
#     - Provide the location and venue details.
#     - Mention the start and end times of the events.
#     - Include any associated costs or ticket prices.
#     - Highlight any unique features or special guests.
#     - Provide links to event websites for more information.

#     Save the report in a clear and organized manner.
#     """
#     return prompt
# # print(prompt_events(query))

# def prompt_final(query, scope) -> str:
#     prompt =  f"""
#         Create a markdown format travel info to {query['name_city']} between {query['date_fr']} and {query['date_to']} based on collected information. 
        
#         Requirements:
#         - Provide general info about {query['name_city']}.
#         - Provide overall fit for turist focused on {query['desc_user']}.
#         - Focus only on collected information.
#         """
#     if scope['eating']: 
#         prompt_add = f"""
#         - Restaurants in {query['name_city']} with information on:
#             reservation requirement, opening hours, cousine, specialities, price range, address.
#         """
#         prompt += prompt_add
#     if scope['events']: 
#         prompt_add = f"""
#         - Events in {query['name_city']} between {query['date_fr']} and {query['date_to']} with information on:
#             reservation requirement, category, time, specialities, unique features, links.
#         """    
#         prompt += prompt_add
#     return prompt
# # print(prompt_final(query, scope))