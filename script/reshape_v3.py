
import matplotlib.pyplot as plt
import geopandas as gpd 
from shapely.geometry import LineString, Polygon, MultiPolygon
from shapely import make_valid
import xarray as xr 
import pandas as pd
import numpy as np 
import json
from pyproj import CRS, Transformer
from shapely.ops import transform
from spilhaus import from_spilhaus_xy_to_lonlat

extreme = 16168767 # pyproj biggest number can be tranfered from 54099 to 4326 
crs_54099 = CRS.from_proj4("+proj=spilhaus +lat_0=-49.56371678 +lon_0=66.94970198 +azi=40.17823482 +k_0=1.4142135623731 +rot=45 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs")
crs_4326 = CRS.from_epsg(4326)
tform = Transformer.from_crs(crs_54099,crs_4326, always_xy = True)
# tform_re = Transformer.from_crs(crs_4326, crs_54099, always_xy=True)
def tx_point(coord):
        x,y = tform.transform(coord[0],coord[1])
        return [x,y]

n1, n2 = -extreme, extreme
n = 200
middle_values = np.linspace(n1, n2, n).tolist()

## 构造 spilhaus north 边界线 - 两个extreme之间插点
y = extreme
points_n = [[x,y] for x in middle_values]
points_wgs_north =[]
for point in points_n:
        coord_new = tx_point(point)
        points_wgs_north.append(coord_new)
# print (points_wgs)

# 构造新的上north边界 
# line_geom_north = LineString(points_wgs_north)
# line_wgs_north = gpd.GeoSeries([line_geom_north], crs = "EPSG: 4326")

## 构造 spilhaus south 边界线 - 两个extreme之间插点
y = -extreme
points_s = [[x,y] for x in middle_values]
points_wgs_south =[]
for point in points_s:
        coord_new = tx_point(point)
        points_wgs_south.append(coord_new)


## 构造 spilhaus west 边界线 - 两个extreme之间插点
x = -extreme
points_w = [[x,y] for y in middle_values]
points_wgs_west =[]
for point in points_w:
        coord_new = tx_point(point)
        points_wgs_west.append(coord_new)


## 构造 spilhaus east 边界线 - 两个extreme之间插点
x = extreme
points_e = [[x,y] for y in middle_values]
points_wgs_east =[]
for point in points_e:
        coord_new = tx_point(point)
        points_wgs_east.append(coord_new)


## 构造geojson 
data = {
  "type": "FeatureCollection",
  "features": [
    {
      "type": "Feature",
        "properties": { "boundary": "north"  },
      "geometry": {
        "type": "LineString",
        "coordinates": points_wgs_north }},
    {
      "type": "Feature",
       "properties": { "boundary": "south" },
      "geometry": {
        "type": "LineString",
        "coordinates": points_wgs_south }},
    {
      "type": "Feature",
       "properties": { "boundary": "west" },
      "geometry": {
        "type": "LineString",
        "coordinates": points_wgs_west }},
    {
      "type": "Feature",
       "properties": { "boundary": "east" },
      "geometry": {
        "type": "LineString",
        "coordinates": points_wgs_east }}
  ]
}

print(data)

with open("/Users/xy/Documents/workspace/SpilhausPolygon/data/boundaries.geojson", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)