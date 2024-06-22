#!/usr/env/bin python3

# Src: https://geopandas.org/en/stable/getting_started/introduction.html

import geopandas
from geodatasets import get_path

path_to_data = get_path("nybb")
gdf = geopandas.read_file(path_to_data)

print(gdf)