from unicodedata import name
import requests


class SWIntegration():
    """Star Wars API"""
    def __init__(self):
        self.base_url = "https://swapi.dev/api/"

    def get_people(self, name_filter=None):
        people_request = requests.get(
            url=f"{self.base_url}/people",
            params={"search": name_filter}
        )

        people_response = people_request.json()
        return people_response["results"]

    def get_character_films(self, title_urls):
        film_data = []
        
        for _ulr in title_urls:
            title_request = requests.get(
                url= _ulr
            )
            film_data.append(title_request.json())
        
        return film_data
