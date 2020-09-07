import requests
from time import sleep

API_URL = "https://restcountries.eu/rest/v2/name/"


def get_countries_info(country_names):
    responses = {}

    for country_name in country_names:
        if country_name not in responses:
            print(f"{API_URL}{country_name}")
            response = requests.get(f"{API_URL}{country_name}")
            if response.status_code == 200:
                response = response.json()
                
                if len(response) == 1:
                    responses[country_name] = response[0]
                else:
                    for obj in response:
                        if obj["name"] == country_name or (country_name in obj["translations"]):
                            responses[country_name] = obj
                            break
                    else:
                        print(f"error {country_name}, {response}")
                        responses[country_name] = response
                        
                
            else:
                print(response.status_code)
                print(country_name)
                print(response.text)
                responses[country_name] = {}
        
        sleep(0.5)
        
        return responses
        

def 
