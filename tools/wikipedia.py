# import wikipediaapi
# from langchain_community.tools import WikipediaQueryRun
# from langchain_community.utilities import WikipediaAPIWrapper

# wikipedia = WikipediaQueryRun(api_wrapper=WikipediaAPIWrapper())
# data_wiki = wikipedia.run(f"{name_city}")

# url = f"https://en.wikipedia.org/wiki/{name_city}"

# def search_wikipedia(query):
#     wiki_wiki = wikipediaapi.Wikipedia('MyProjectName (merlin@example.com)', 'en')

#     search_results = wiki_wiki.search(query)

#     # Store results
#     results = []

#     # Loop through the search results
#     for title in search_results:
#         # Fetch the page for the given title
#         page = wiki_wiki.page(title)
        
#         # Check if the page exists
#         if page.exists():
#             # Append the title and a brief summary to the results list
#             results.append({
#                 'title': title,
#                 'summary': page.summary[:500]  # Limiting to the first 500 characters for brevity
#             })
    
#     return results

# data_wiki = [{
#     'Title': f"{result['title']}",
#     'Summary': f"{result['summary']}",
#     'URL': f"{result['url']}",
#     } for result in results]
