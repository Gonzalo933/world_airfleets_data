import sys

import requests
from bs4 import BeautifulSoup


def parse_plane(plane_url, plane_name):
    response = requests.get(plane_url)

    if not response.ok:
        print("Error")
        return None

    plane_html = response.content
    soup = BeautifulSoup(plane_html, "html.parser")

    plane_rows = soup.find_all("tr", {"class": "trtab"})
    cells_titles = ["msn", "type", "airline", "first_flight", "registration", "status"]
    planes_matrix = []
    for row in plane_rows:
        cells = row.find_all("td")
        plane_row = []
        plane_row.append(plane_name)
        for cell_and_title in zip(cells, cells_titles):
            text = cell_and_title[0].text.strip()
            title = cell_and_title[1]
            plane_row.append(text)
        planes_matrix.append(plane_row)
    return planes_matrix
