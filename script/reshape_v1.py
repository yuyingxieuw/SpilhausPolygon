import json
import shapely
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

## 用函数来返回

## 函数用来返回坐标象限
# data in - a polygon list []传入一个lat lng左边
# data out - 1，2，3，4 传出一个象限值
def quad_sign_check(coord):
    #包括在x轴右边
    if coord[0]>0 and coord[1]>=0:
        return 1
    #包括在y轴上面
    elif coord[0]<=0 and coord[1]>0:
        return 2
    #包括在x轴左边
    elif coord[0]<0 and coord[1]<=0:
        return 3
    #包括在y轴下面
    elif coord[0]>=0 and coord[1]<0:
        return 4

## 计算一个ring的平均点间距
def cal_avg_dist(ring):
    distance = []
    for i in range (len(ring)-1):
        p1, p2 = ring[i], ring[i+1]
        dist = math.dist(p1,p2)
        distance.append((i,dist))
    avg_dist=sum(d for _, d in distance) / len(distance)
    return avg_dist
    

## 检测断点之间的距离是不是比这个点与其他点之间的距离大很多
# 传入检测的ring 也就是polygon, 和断点第几
def point_change_big(ring,s,avg_distance,threshold):
    breakpoint_dist = math.dist(ring[s-1],ring[s])
    if breakpoint_dist > avg_distance*(1+threshold):
        return True
    else:
        return False

##function改写成function来找到象限变换的断点
#传入一个feature的all coord(很多polygon)
#return split字典：哪个polygon 第几个值变换
def find_breakpoint(all_coord,f):
    split={}
    for i, p in enumerate(all_coord):
        #提取每一个polygon的ring(如果有hole的话也只提取第一个ring)
        ring = p[0]
        #计算ring的平均点间距-后面用
        avg_distance=cal_avg_dist(ring)
        #检查是不是有hole 此处先不处理hole
        if len(p) >1:
            print(f"Number{i} polygon has a hole")
        #检查是不是坐标轴变化
        #每次储存
        quad = {}
        split_point =[]
        for s, coord in enumerate(ring):
            sign = quad_sign_check(coord)
            quad[s] = sign
            if s > 0: 
                t = s-1
                ##点间距检测是否异常
                far = point_change_big(ring,s,avg_distance,threshold=2)
                ## 检测是否变换且是1/3； 2/4 变换
                if (quad[s]!= quad[t] and quad[s]* quad[t]in(3,8)) or (quad[s] != quad[t] and quad[s] * quad[t]in(4,12,6,2) and far):
                    #print (f"第{i}polygon, 第{s} ring, quad sign changed at {s} from 象限{quad[t]} to 象限{quad[s]}")
                    split_point.append (s)
                else:
                    continue
        #print(split_point)
        if split_point:
            split[i]=split_point
        elif not split_point:
            pass
    print(f"--------all change points in No{f} feature in this data----------")
    print(split)
    return split

## function重新组织生成新的coord
#传入split字典（哪个polygon哪个值改变）
#传出新的polygon
def remake_polygon(split,all_coord):
    remake_poly = {}
    for i, (k,v) in enumerate(split.items()):
        #提取有断点的poly
        poly = all_coord[k]
        #先不管hole
        ring = poly[0]
        #增加最后一个点
        v.append(len(ring))
        #print("------poly index, poly number, split coord index -------")
        #print (i,k,v)
        split_poly = []
        for n, p in enumerate(v):
            new_poly = []
            if n == 0:  
                for a in range(0,p,1):
                    new_poly.append(ring[a])
                new_poly.append(ring[0])
            if n != 0:
                for a in range(v[n-1],p,1):
                    new_poly.append(ring[a])
                new_poly.append(ring[v[n-1]])
            split_poly.append(new_poly)
        remake_poly[k] = split_poly
    return remake_poly

## 放入原有的结构（一个feature）
# 传入被remake poly 修正过的新的coord
# 传入原始data
# 传出新的geojson
def restructure_coords(remake_poly,data,i):
    for t, coord in remake_poly.items():
        if data.get("type") == "FeatureCollection":
            data.get("features")[i].get("geometry").get("coordinates")[t] = remake_poly[t]
        elif data.get("type") == "Feature":
            data.get("geometry").get("coordinates")[t] = remake_poly
    return data

## 写入新的data
def write_data_to_file(new_data):
    with open ("make_valid.geojson", "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=2) 

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
            split = find_breakpoint(all_coord, f) #检查是否更改坐标
            far = None #检查是否很远
            #如果split, across, far 都满足，再切割
            if split:
                remake_poly = remake_polygon(split,all_coord)
                new_data = restructure_coords(remake_poly,data,f)
            elif not split:
                pass
        write_data_to_file(new_data)
        
    elif data.get("type") == "Feature":
        all_coord = data.get("geometry").get("coordinates")
        split = find_breakpoint(all_coord)
        across = None #检查是否across象限
        far = None #检查是否很远
        #如果split, across, far 都满足，再切割
        if split:
            remake_poly = remake_polygon(split,all_coord)
            new_data = restructure_coords(remake_poly,data,0)
            write_data_to_file(new_data)
        elif not split:
            pass
            
## 运行main
if __name__=="__main__":
    main()