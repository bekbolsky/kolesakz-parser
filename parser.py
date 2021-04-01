import csv
import re
from random import uniform
import time
from typing import List, Tuple


import requests
from bs4 import BeautifulSoup
from bs4.element import ResultSet, Tag
from tqdm import trange


BASE_URL = "https://kolesa.kz"
URL = f"{BASE_URL}/spectehnika/gruzoviki/region-zhambilskaya-oblast/"
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
    html = response.text
    return html


def pages_count(html: str) -> int:
    soup = BeautifulSoup(html, "lxml")
    paginator = soup.find("div", {"class": "pager"}).find_all("li")

    if paginator:
        last_page = int(paginator[-1].text.strip())
    else:
        last_page = 1
    return last_page


def gather_valuable_data(advert: Tag) -> Tuple[str, ...]:
    engine_volume_pattern = re.compile(r"(^\d+.*)(\s)(л$)")
    fuels = ("бензин", "дизель", "газ-бензин", "газ", "гибрид", "электричество")

    vehicle_mark = " ".join(
        advert.find("span", {"class": "a-el-info-title"}).text.split()[:3]
    )
    price = "".join(advert.find("span", {"class": "price"}).text.split()[:-1])
    emergency = advert.find("span", {"class": "emergency"}).text.split(",")[0]
    description = (
        advert.find("div", {"class": "a-search-description"})
        .text.strip()
        .split(",")[:6]
    )
    year = description[0].strip()

    if (
        description[1].strip() not in fuels
        and re.match(engine_volume_pattern, description[1].strip()) is None
    ):
        vehicle_type = description[1].strip()
    else:
        vehicle_type = ""

    if re.match(engine_volume_pattern, description[2].strip()):
        engine_volume = description[2].strip()
    elif re.match(engine_volume_pattern, description[1].strip()):
        engine_volume = description[1].strip()
    else:
        engine_volume = ""

    fuel_type = ""
    for target in description[1:]:
        if target.strip() in fuels:
            fuel_type = target.strip()

    data = (
        vehicle_mark,
        year,
        price,
        emergency,
        fuel_type,
        engine_volume,
        vehicle_type,
    )

    return data


def collect_data(adverts: ResultSet) -> List:
    collection = []
    for ad in adverts:
        try:
            data = gather_valuable_data(ad)
            collection.append(data)
        except AttributeError:
            continue
        except IndexError:
            continue
    return collection


def save_data(filename, data: List) -> None:
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


def main():
    last_page = pages_count(get_html(URL))

    data_collection = []
    for i in trange(1, last_page + 1, desc="Progress"):
        html = get_html(f"{URL}?page={i}")
        soup = BeautifulSoup(html, "lxml")
        ads_list = soup.find_all("div", {"class": "a-elem"})
        data = collect_data(ads_list)
        data_collection.extend(data)
        rand_sec = round(uniform(0.4, 1), 2)
        time.sleep(rand_sec)

    save_data("pretty_data.csv", data_collection)


if __name__ == "__main__":
    main()
