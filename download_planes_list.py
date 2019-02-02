import sys

import requests
from bs4 import BeautifulSoup
from lxml import etree


def download_plane_list(base_url):
    plane_list_url = f"{base_url}/recherche/supported-plane.htm"
    response = requests.get(plane_list_url)

    if not response.ok:
        print("Error")
        sys.exit(1)

    # html of webpage
    plane_list_webpage_content = response.content

    data = etree.HTML(plane_list_webpage_content)
    # xpath of the table with the list of the planes
    planes_table = data.xpath("/html/body/table[4]/tr[1]/td/table/tr/td[3]/table")[0]
    planes_table_html = etree.tostring(planes_table)  # pretty_print=True

    soup = BeautifulSoup(planes_table_html, "html.parser")
    rows = soup.find_all("tr")
    planes = []
    for row in rows:
        # Extract plane name and url from anchor
        plane_anchor = row.find_all("a")
        if plane_anchor:
            plane_name = plane_anchor[0].text
            link = plane_anchor[0]["href"].replace("..", "")
            planes.append([plane_name, link])
            # print(plane_name)
    return planes
