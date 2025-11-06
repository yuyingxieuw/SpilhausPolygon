import json
import shapely
from shapely.validation import make_valid
from shapely.validation import explain_validity
from shapely.geometry import mapping, shape, Polygon, Point
import numpy as np
import math
from shapely.ops import transform

extreme = {
    "xmax" : 16689359.762781348,
    "ymax" : 16691089.441339396,
    "xmin" : -16689689.72942762,
    "ymin" : -16690292.833040055
}

offshore = extreme["xmax"]*0
extreme_smaller = {
    "xmax" : extreme["xmax"]-offshore,
    "ymax" : extreme["ymax"]-offshore,
    "xmin" : extreme["xmin"]+offshore,
    "ymin" : extreme["ymin"]+offshore
}
## this script reconstruct polygon
def load_geojson_to_data(inpath):
    with open (inpath, "r", encoding = "utf-8") as f:
        data = json.load(f)
    return data

##找到触碰边界的点。
def find_breakpoint(ring,offshore):
    """
    Find point touch the extreme boundarys
    
    :param all_coord: geometory of a ring
    :param offshour: adjust the size of extreme from startard
    :return: split dic, which polygon, which point.
    """
    split_point =[]
    for s, coord in enumerate(ring):
        x,y = coord
        if not (extreme_smaller["xmin"] <= x <= extreme_smaller["xmax"] and 
            extreme_smaller["ymin"] <= y <= extreme_smaller["ymax"]):
            split_point.append([s, coord])
        else:
            continue
    return split_point


##找关于质心极角差大于90度的点
def find_crosspoint(ring):
    pts = np.array(ring)
    cx,cy = pts.mean(axis = 0)
    dx = pts[:,0] - cx
    dy = pts[:,1] - cy
    angles = np.arctan2(dy,dx)
    
    # detect sudden angle jump > pi/2
    for i in range (len(angles)-1):
        if angles[i+1] - angles[i] > np.pi/2:
            print (f"Jump at index {i}: {angles[i]} -> {angles[i+1]}")

##重组polygon
def reconstruct_polygon(ring):
    pass

## main app
def main(): 
    inpath = "/Users/xy/Documents/workspace/SpilhausPolygon/data/rawChina54099.geojson"
    data= load_geojson_to_data(inpath)
    if data.get("type") == "FeatureCollection":
        all_data = data.get("features")
        print(f"整个数据结构有{len(all_data)}feature")
        for f,dic in enumerate(all_data):
            # f 也是第几个feature
            all_coord = dic.get("geometry").get("coordinates")
            for i,p in enumerate(all_coord):
                #i 是第几个polygon 
                ring = p[0] # 只取第一个ring（忽略hole）
                if len(p) >1:
                    print(f"Number{i} polygon in feature {f} has a hole")
                #针对每个polygon检测(ring == polygon)
                print(f"检测第{f}个feature,第{i}个polygon")
                find_breakpoint(ring,offshore=offshore) #检查是否触碰边界
                find_crosspoint(ring) #检测偏离质心大于90度
                reconstruct_polygon(ring) #重构每个ring         
        
    elif data.get("type") == "Feature":
        all_coord = data.get("geometry").get("coordinates")
        find_breakpoint(all_coord) 
        
        
            
## 运行main
if __name__=="__main__":
    main()