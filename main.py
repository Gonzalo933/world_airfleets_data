import os
import time

import numpy as np
import pandas as pd

from download_plane_data import parse_plane
from download_planes_list import download_plane_list

base_url = "https://www.airfleets.net"
# List of the plane models to parse
plane_list_file = "planes_list.csv"
# Actual file to store data from
# every plane in the webpage
planes_file = "planes.csv"

# If we already have the list of planes open it
# Otherwise create the list extracting it from the webpage
if not os.path.isfile(plane_list_file):
    planes = download_plane_list(base_url)
    df = pd.DataFrame(planes, columns=["plane_name", "link"])
    df.to_csv(plane_list_file, index=True)

df = pd.read_csv(plane_list_file)

planes_matrix = df.as_matrix()
# Continue progress if the data file already exists
# By checking last plane downloaded.
if not os.path.isfile(planes_file):
    df_planes = pd.DataFrame(
        columns=("plane_name", "msn", "type", "airline", "first_flight", "registration", "status")
    )
    df_planes.to_csv(planes_file, index=False)
else:
    last_plane_scrapped = pd.read_csv(planes_file)["plane_name"].values[-1]
    index = df[df["plane_name"] == last_plane_scrapped].index[-1] + 1
    print(f"Starting at {planes_matrix[index, 1]}")
    planes_matrix = planes_matrix[index:]

for plane in planes_matrix:
    planes_data = []
    empty_page = False
    page_number = 1
    plane_data_url = f"{base_url}{plane[2]}"
    plane_name = plane[1]
    # Loop over page numbers
    while not empty_page:
        plane_page_data = parse_plane(plane_data_url, plane_name)
        time.sleep(3)
        page_number += 1
        plane_data_url = plane_data_url.replace(f"{page_number - 1}.htm", f"{page_number}.html")
        if not plane_page_data:
            empty_page = True
        else:
            planes_data += plane_page_data
    # Save current data
    df_planes = pd.DataFrame(
        planes_data,
        columns=("plane_name", "msn", "type", "airline", "first_flight", "registration", "status"),
    )
    pd.concat([pd.read_csv(planes_file), df_planes]).to_csv(planes_file, index=False, header=True)
    print(f"{plane_name}")
