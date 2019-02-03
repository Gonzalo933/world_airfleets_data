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
    # Sometimes the tables will have more columns than expected so we have to
    # check that we download the ones we want
    cells_titles = ["msn", "type", "airline", "first flight", "registration", "status"]

    table_header_row = soup.find("tr", {"class": "textenu"}).find_all("td")
    parsed_cell_titles = []
    for header_col in table_header_row:
        parsed_cell_titles.append(header_col.text.strip())

    planes_matrix = []
    for row in plane_rows:
        cells = row.find_all("td")
        plane_row = []
        plane_row.append(plane_name)
        for cell_and_title in zip(cells, parsed_cell_titles):
            title_currently_parsing = cell_and_title[1].lower()
            # If this is an extra column that we don't want, skip it
            if not title_currently_parsing in cells_titles:
                continue
            text = cell_and_title[0].text.strip()
            plane_row.append(text)
        planes_matrix.append(plane_row)
    return planes_matrix
