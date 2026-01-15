import json

from shapely.validation import make_valid
from shapely.validation import explain_validity
from shapely.geometry import mapping, shape, Polygon, Point
import numpy as np
import math
from shapely.ops import transform


## this script reconstruct polygon
def load_geojson_to_data(inpath):
    with open (inpath, "r", encoding = "utf-8") as f:
        data = json.load(f)
    return data

##找到触碰边界的点。
def find_breakpoint(ring,offshore=60000):
    """
    Find point touch the extreme boundarys
    
    :param all_coord: geometory of a ring
    :param offshour: adjust the size of extreme from startard
    :return: split dic, which polygon, which point.
    """
    extreme = {
    "xmax" : 16689359.762781348,
    "ymax" : 16691089.441339396,
    "xmin" : -16689689.72942762,
    "ymin" : -16690292.833040055
    }

    extreme_smaller = {
    "xmax" : extreme["xmax"]-offshore,
    "ymax" : extreme["ymax"]-offshore,
    "xmin" : extreme["xmin"]+offshore,
    "ymin" : extreme["ymin"]+offshore
    }

    split_point =[]
    for s, coord in enumerate(ring):
        x,y = coord
        if not (extreme_smaller["xmin"] < x < extreme_smaller["xmax"] and 
            extreme_smaller["ymin"] < y < extreme_smaller["ymax"]):
            split_point.append([s, coord])
        else:
            continue
    #print(split_point)
    return split_point

# 找一个feature 所有polygon(拆分点集)的几何中心
def find_center_forall(all_coord):
    all_points = [ring 
                  for poly in all_coord 
                  for ring in poly[0]]
    pts = np.array(all_points)
    cx_all, cy_all = pts.mean(axis = 0)
    return [cx_all, cy_all]

##找关于质心极角差大于90度的点
def find_crosspoint(ring,center_all):
    cross_point = {}
    pts = np.array(ring)
    #cx,cy = pts.mean(axis = 0)
    #print(f"center point for the current polygon {cx,cy}")
    cx,cy=center_all
    dx = pts[:,0] - cx
    dy = pts[:,1] - cy
    angles = np.arctan2(dy,dx)
    
    # detect sudden angle jump > pi/2
    for i in range (len(angles)-1):
        a,b=angles[i],angles[i+1]
        diff =abs(a-b)
        if min(diff,2*np.pi-diff) > np.pi/2:
            print (f"Jump at index {i}: {angles[i]} -> {angles[i+1]}")
            cross_point[i] = ring[i]
    return cross_point

##重组polygon
def reconstruct_polygon(ring, cross_point):
    # 根据break point 分成线段
    # 如果一个ring/plygon 有两个break point 说名有两条飞线
    pass

## main app
def main(): 
    inpath = "/Users/xy/Documents/workspace/SpilhausPolygon/data/rawChina54099.geojson"
    data= load_geojson_to_data(inpath)
    all_crosspoint = {}
    if data.get("type") == "FeatureCollection":
        all_data = data.get("features")
        print(f"整个数据结构有{len(all_data)}feature")
        for f,dic in enumerate(all_data):
            # f 也是第几个feature
            all_coord = dic.get("geometry").get("coordinates")
            # 找所有点的几何中心
            center_all = find_center_forall(all_coord)
            print("-------------all points flattened Centorid--------------")
            print(center_all)
            for i,p in enumerate(all_coord):
                #i 是第几个polygon 
                ring = p[0] # 只取第一个ring（忽略hole）
                if len(p) >1:
                    print(f"Number{i} polygon in feature {f} has a hole")
                #针对每个polygon检测(ring == polygon)
                print(f"检测第{f}个feature,第{i}个polygon")
                find_breakpoint(ring,offshore=16689359*0.000) #检查是否触碰边界
                cross_point = find_crosspoint(ring,center_all)
                if cross_point: #检测偏离质心大于90度 
                    all_crosspoint [i] = cross_point
                    reconstruct_polygon(ring,cross_point) #重构每个ring/poly
    print("EXAM FINISHED ------ All CROSS POINTS -------")
    print (all_crosspoint)
        
    # elif data.get("type") == "Feature":
    #     all_coord = data.get("geometry").get("coordinates")
    #     find_breakpoint(all_coord) 
                
            
## 运行main
if __name__=="__main__":
    main()