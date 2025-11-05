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

#计算一个ring最小/大点距
def cal_minmax_dist(ring):
    distance = []
    for i in range(len(ring)-1):
        p1,p2=ring[i], ring[i+1]
        dist = math.dist(p1,p2)
        distance.append(dist)
    return max(distance)

##找到触碰边界的点。
#传入一个feature的all coord(很多polygon)
#return split字典：哪个polygon 第几个值变换
def find_breakpoint(all_coord,offshore):
    split={}
    for i, p in enumerate(all_coord): #循环for 每一个polygon
        #提取每一个polygon的ring(如果有hole的话也只提取第一个ring)
        ring = p[0]
        #检查是不是有hole 此处先不处理hole
        if len(p) >1:
            print(f"Number{i} polygon has a hole")
        #检查是不是在边界外
        #每次储存
        split_point =[]
        for s, coord in enumerate(ring):
            x,y = coord
            if not (extreme_smaller["xmin"] <= x <= extreme_smaller["xmax"] and 
                extreme_smaller["ymin"] <= y <= extreme_smaller["ymax"]):
                split_point.append([s, coord])
            else:
                continue
        #print(split_point)
        if split_point:
            split[i]=split_point
        elif not split_point:
            continue
    print(f"--------all touch boundary points in this data with offshore {offshore}----------")
    print(split)
    return split

#找极端值 
#传入一个feature的all coord(很多polygon)
#return split字典：哪个polygon 第几个值变换
def find_outliner(all_coord):
    outliner={}
    max_list=[]
    for i, p in enumerate(all_coord): #循环for 每一个polygon
        #提取每一个polygon的ring(如果有hole的话也只提取第一个ring)
        ring = p[0]
        #检查是不是有hole 此处先不处理hole
        if len(p) >1:
            print(f"Number{i} polygon has a hole")
        #检查是不是坐标轴变化
        #每次储存
        max = cal_minmax_dist(ring)
        max_list.append(max)
    print (sorted(max_list))
        

## 主程序
def main(): 
    inpath = "/Users/xy/Documents/workspace/widget-spilhaus/data/rawChina54099.geojson"
    data= load_geojson_to_data(inpath)
    if data.get("type") == "FeatureCollection":
        all_data = data.get("features")
        print(f"整个数据结构有{len(all_data)}feature")
        for f,dic in enumerate(all_data):
            # i 也是第几个feature
            all_coord = dic.get("geometry").get("coordinates")
            find_breakpoint(all_coord,offshore=offshore) #检查是否触碰边界
            find_outliner(all_coord) #检查是否极端值
            
        
    elif data.get("type") == "Feature":
        all_coord = data.get("geometry").get("coordinates")
        find_breakpoint(all_coord) 
        find_outliner(all_coord)
        
            
## 运行main
if __name__=="__main__":
    main()