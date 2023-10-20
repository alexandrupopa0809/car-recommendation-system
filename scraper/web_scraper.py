import requests
from bs4 import BeautifulSoup
import re
import json
import pandas as pd
import logging
import time


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)


URL = "https://www.autovit.ro/autoturisme?page={}"
SCRIPT_ID = "__NEXT_DATA__"
URL_PATTERN = r"https://www\.autovit\.ro/autoturisme/anunt/.*?\.html"
NUM_PAGES = 1000

CAR_FEATURES = [
        "make",
        "model",
        "year",
        "mileage",
        "fuel_type",
        "engine_power",
        "engine_capacity",
        "transmission",
        "pollution_standard",
        "gearbox",
        "body_type",
        "country_origin",
        "original_owner",
        "no_accident",
    ]


def get_other_car_details(details):
    car_values = []
    for key in CAR_FEATURES:
        for detail_obj in details:
            if key == detail_obj["key"]:
                car_values.append((key, detail_obj["value"]))
                break
    return car_values


def create_dataframe(data_list):
    """
    data_list is a list of lists of tuples. Each list represents an example,
    the first item from the tuple should be the label of the dataframe and
    the second item should be the value.
    """
    data_dict = {}
    labels = ["title", "price"] + CAR_FEATURES
    for label in labels:
        data_dict[label] = []

    for car_example in data_list:
        temp_dict = {key: value for key, value in car_example}
        for label in labels:
            data_dict[label].append(temp_dict.get(label, None))
    df = pd.DataFrame(data_dict)
    return df


if __name__ == "__main__":
    all_data = []
    for page_number in range(1, NUM_PAGES + 1):
        response = requests.get(URL.format(page_number))
        if response.status_code == 200:
            logging.info(f"Scraping cars from autovit page {page_number}...")
            page_soup = BeautifulSoup(response.text, "html.parser")
            page_info = page_soup.find("script", id=SCRIPT_ID)
            car_urls = re.findall(URL_PATTERN, str(page_info))

            for car_url in car_urls:
                car_response = requests.get(car_url)
                if car_response.status_code == 200:
                    car_soup = BeautifulSoup(car_response.text, "html.parser")
                    try:
                        car_info = json.loads(car_soup.find("script", id=SCRIPT_ID).text)
                    except AttributeError:
                        continue
                    try:
                        title = car_info["props"]["pageProps"]["advert"]["title"]
                        price = car_info["props"]["pageProps"]["advert"]["price"]["value"]
                        details = car_info["props"]["pageProps"]["advert"]["details"]
                    except KeyError:
                        logging.warning("Key error: %s", car_url)
                        continue

                    other_car_details = get_other_car_details(details)
                    row_example = [("title", title), ("price", price)] + other_car_details
                    all_data.append(row_example)

        if page_number % 100 == 0:
            df = create_dataframe(all_data)
            df.to_csv(f"car_records_{page_number}.csv")
            all_data = []

            logging.info(f"Scraping successfully completed for the first {page_number} pages!")
            logging.info("Sleeping...")
            time.sleep(600)
            logging.info("Sleeping done!")
