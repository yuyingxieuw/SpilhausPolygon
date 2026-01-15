from spilhaus import from_lonlat_to_spilhaus_xy
from spilhaus import make_spilhaus_xy_gridpoints
from reshape_v2 import find_crosspoint
import matplotlib.pyplot as plt
import geopandas as gpd 
from shapely.geometry import Polygon, MultiPolygon
from shapely import make_valid
import xarray as xr 
import pandas as pd
import numpy as np 
import json
import pyproj
from reshape_v2 import find_breakpoint


inpath = "/Users/xy/Documents/workspace/SpilhausPolygon/data/test.geojson"
# test_4326 = gpd.read_file(inpath)
# test_4326.plot(color="black", edgecolor="black")

with open (inpath, "r", encoding = "utf-8") as f:
    test = json.load(f)
# print(test)
poly = test.get("features")[0].get("geometry")
ring = poly.get("coordinates")

coords = ring[0][0]
# print (coords)
split = find_breakpoint(coords)
print (split)




# china_4236 = gpd.read_file(inpath)
# spilhaus_crs = "ESRI:54099"
# china_54099 = china_4236.to_crs(spilhaus_crs)
# china_valid = china_54099.make_valid()
# print(f"Is valid: {china_valid.is_valid}")
# china_4326.plot(color="black", edgecolor="white")
# extreme = 11825474
# mask_coords = [
#     (-extreme, -extreme),
#     (extreme, -extreme),
#     (extreme, extreme),
#     (-extreme, extreme)
# ]

# clip_poly = Polygon(mask_coords)
# mask_gdf = gpd.GeoDataFrame({'geometry': [clip_poly]}, crs = spilhaus_crs)

# land_prettified = gpd.clip(china_54099, mask_gdf)