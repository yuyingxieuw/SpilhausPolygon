from spilhaus import from_lonlat_to_spilhaus_xy
import matplotlib.pyplot as plt
import geopandas as gpd 
from shapely.geometry import Polygon, MultiPolygon
import xarray as xr 
import pandas as pd
import numpy as np 
import json

inpath = "/Users/xy/Documents/workspace/SpilhausPolygon/data/simpleChina4326.geojson"

gdf = gpd.read_file(inpath)
# print (gdf.geometry.name)
# print(gdf.columns)

geom = gdf.geometry.iloc[0] #取出第 0 行 feature 的 geometry（一个 Shapely 几何对象）
# print(geom)
print(geom.geom_type)
geom.geoms   # tuple of Polygon - object 
print(geom.geoms) # object
print(len(geom.geoms)) # how many does it have 
ext_coords = [list(poly.exterior.coords) for poly in geom.geoms]
#holes = [[list(poly.coords) for ring in poly.interiors]for poly in geom.geoms]
# print("______________exterior_________")
# print(ext_coords)
# print(len(ext_coords))
#print("______________holes____________")
#print(holes)

ext_0 = ext_coords[0] # 第一个exterior
ext_1 = ext_coords[1]
#print(ext_0)
coord_array_0 = np.array(ext_0)
x_array_0 = coord_array_0[:,0]
y_array_0 = coord_array_0[:,1]
spil_x, spil_y = from_lonlat_to_spilhaus_xy(x_array_0, y_array_0)
poly_0 = list(zip(spil_x.tolist(), spil_y.tolist()))
print("________________________result0 ________________________________")
print(poly_0)

coord_array_1 = np.array(ext_1)
x_array_1 = coord_array_1[:,0]
y_array_1 = coord_array_1[:,1]
spil_x_1, spil_y_1 = from_lonlat_to_spilhaus_xy(x_array_1, y_array_1)
poly_1 = list(zip(spil_x_1.tolist(), spil_y_1.tolist()))
print("________________________result1 ________________________________")
print(poly_1)

poly1 = Polygon(poly_0)
poly2 = Polygon(poly_1)
new_geom = MultiPolygon([poly1, poly2])
gdf.loc[0, "geometry"] = new_geom