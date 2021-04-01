import csv
import re
from random import uniform
import time


import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet
from tqdm import trange


URL = "https://kolesa.kz/spectehnika/gruzoviki/samosval/region-zhambilskaya-oblast/"
HEADERS = {
    "accept": "*/*",
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
    " AppleWebKit/537.36 (KHTML, like Gecko) "
    "Chrome/89.0.4389.90 Safari/537.36",
}


def get_html(url: str) -> str:
    """Takes the URL as an argument for the request,
    returns the html page from the request.

    Uses `get()` method from `requests` package

    Args:
        url ([str]): [link to the website]

    Returns:
        [str]: [HTML page from the request]
    """
    response = requests.get(url, headers=HEADERS)
    return response.text


def pages_count(html: str) -> int:
    soup = BeautifulSoup(html, "lxml")
    paginator = soup.find("div", {"class": "pager"}).find_all("li")

    if paginator:
        last_page = int(paginator[-1].text.strip())
    else:
        last_page = 1
    return last_page


def gather_data(adverts: ResultSet) -> list:
    data = []
    engine_volume_pattern = re.compile(r"(^\d+.*)(\s)(л$)")
    for ad in adverts:
        try:
            vehicle_mark = " ".join(
                ad.find("span", {"class": "a-el-info-title"}).text.split()[:3]
            )
            price = "".join(ad.find("span", {"class": "price"}).text.split()[:-1])
            emergency = ad.find("span", {"class": "emergency"}).text.split(",")[0]
            description = (
                ad.find("div", {"class": "a-search-description"})
                .text.strip()
                .split(",")[:6]
            )
            year = description[0].strip()
            vehicle_type = description[1].strip()
            engine_volume = (
                description[2].strip()
                if re.match(engine_volume_pattern, description[2].strip())
                else ""
            )
            if engine_volume != "":
                fuel_type = description[3].strip()
            elif emergency == description[2].strip():
                fuel_type = ""
            elif len(description[2].strip()) > 13:
                fuel_type = ""
            else:
                fuel_type = description[2].strip()
            data.append(
                [
                    vehicle_mark,
                    year,
                    price,
                    emergency,
                    fuel_type,
                    engine_volume,
                    vehicle_type,
                ]
            )
        except AttributeError:
            continue
        except IndexError:
            continue
    return data


last_page = pages_count(get_html(URL))

data_collection = []

for i in trange(1, last_page + 1, desc="Progress"):

    site_response = get_html(f"{URL}?page={i}")
    soup_object = BeautifulSoup(site_response, "lxml")
    # print(f"Page parsing: {i} of {last_page}. Amount remaining: {last_page-i}")

    ads_list = soup_object.find_all("div", {"class": "a-elem"})
    data = gather_data(ads_list)
    data_collection.extend(data)

    rand_sec = round(uniform(0.4, 1), 2)
    # print(f"sleeping for {rand_sec} secs")
    time.sleep(rand_sec)


def save_data(filename, data: list):
    with open(filename, "wt", encoding="utf-8") as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(
            (
                "vehicle",
                "year",
                "price",
                "emergency",
                "fuel_type",
                "engine_volume",
                "vehicle_type",
            )
        )

        for row in data:
            writer.writerow(row)


save_data("data.csv", data_collection)
