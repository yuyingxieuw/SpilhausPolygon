from pyproj import CRS, Transformer
import shapely
import json 
from spilhaus import from_lonlat_to_spilhaus_xy

## this is the code transform coord data from 4326 to spilhaus
def transform(in_path):
    crs_54099 = CRS.from_proj4("+proj=spilhaus +lat_0=-49.56371678 +lon_0=66.94970198 +azi=40.17823482 +k_0=1.4142135623731 +rot=45 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs")
    crs_4326 = CRS.from_epsg(4326)
    tform = Transformer.from_crs(crs_4326, crs_54099, always_xy = True)

    def tx_point(coord):
        x,y = tform.transform(coord[0],coord[1])
        return [x,y]
    
    with open(in_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for feature in data.get("features"):
        coords = feature.get("geometry").get("coordinates") 
        feature["geometry"]["coordinates"] = [[[tx_point(pt) for pt in ring] for ring in poly]for poly in coords]

    return data


def save_to_file(data, out_path):
    with open (out_path, "w", encoding="utf-8") as f:
        json.dump(data,f,ensure_ascii=False, indent=2)

def getbound():
    crs_54099 = CRS.from_proj4("+proj=spilhaus +lat_0=-49.56371678 +lon_0=66.94970198 +azi=40.17823482 +k_0=1.4142135623731 +rot=45 +x_0=0 +y_0=0 +datum=WGS84 +units=m +no_defs +type=crs")
    crs_4326 = CRS.from_epsg(4326)
    tform = Transformer.from_crs(crs_4326, crs_54099, always_xy = True)
    x,y = tform.transform(-65,-30)
    print (x,y)

def main():
    inpath = "/Users/xy/Documents/workspace/SpilhausPolygon/data/SimpleRussia4326.geojson"
    data = transform(inpath)
    # if not checkvalid(data):
    #     data_fixed = fixgeojson()
    # else:
    #     return data
    save_to_file(data,"data/rawRussia54099.geojson")
    getbound()



if __name__ == "__main__":
    main()
