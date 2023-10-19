import requests
from bs4 import BeautifulSoup
import re
import json


URL = "https://www.autovit.ro/autoturisme?page={}"
SCRIPT_ID = "__NEXT_DATA__"
URL_PATTERN = r"https://www\.autovit\.ro/autoturisme/anunt/.*?\.html"
NUM_PAGES = 500


if __name__ == '__main__':
    response = requests.get(URL.format(1))
    if response.status_code == 200:
        page_soup = BeautifulSoup(response.text, "html.parser")
        page_info = page_soup.find("script", id=SCRIPT_ID)
        car_urls = re.findall(URL_PATTERN, str(page_info))
        
        for car_url in car_urls:
            print(car_url)
            car_response = requests.get(car_url)
            if car_response.status_code == 200:
                car_soup = BeautifulSoup(car_response.text, "html.parser")
                car_info = car_soup.find("script", id=SCRIPT_ID)
                if car_info:
                    with open("car_json.json", "w") as f:
                        f.write(str(car_info))
                    break                    

