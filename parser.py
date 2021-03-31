import csv
import re

import requests
from bs4 import BeautifulSoup


URL = "https://kolesa.kz/spectehnika/gruzoviki/samosval/"
HEADERS = {
    "Accept": "*/*",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/89.0.4389.90 Safari/537.36",
}

site_response = requests.get(url=URL, headers=HEADERS)
soup_object = BeautifulSoup(site_response.text, "lxml")

catalog = soup_object.find_all("div", {"class": "a-elem"})

engine_volume_pattern = re.compile(r"(^\d+.*)(\s)(л$)")
# print(catalog[0].find('div', {'class': 'a-search-description'}).text.strip().split(',')[2].strip())

csv_file = open("data.csv", "wt", encoding="utf-8")

try:
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

    for item in catalog:
        try:
            vehicle_mark = " ".join(
                item.find("span", {"class": "a-el-info-title"}).text.split()
            )
            price = "".join(item.find("span", {"class": "price"}).text.split()[:-1])
            emergency = item.find("span", {"class": "emergency"}).text.split(",")[0]
            description = (
                item.find("div", {"class": "a-search-description"})
                .text.strip()
                .split(",")
            )
            year = description[0].strip()
            vehicle_type = description[1].strip()
            engine_volume = (
                description[2].strip()
                if re.match(engine_volume_pattern, description[2].strip())
                else ""
            )
            fuel_type = (
                description[3].strip()
                if engine_volume != ""
                else description[2].strip()
            )
            writer.writerow(
                (
                    (
                        vehicle_mark,
                        year,
                        price,
                        emergency,
                        fuel_type,
                        engine_volume,
                        vehicle_type,
                    )
                )
            )
        except AttributeError as e:
            continue
finally:
    csv_file.close()
