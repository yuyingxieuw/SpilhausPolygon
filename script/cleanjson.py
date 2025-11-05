import json

with open ("/Users/xy/Documents/workspace/widget-spilhaus/rewound-geojson.json", "r", encoding="utf-8") as f:
    data = json.load(f)

valid_feature = []

for i, feature in enumerate(data.get("features")): # 返回每个feature dic
    coord = feature.get("geometry").get("coordinates")
    ring = [ring for poly in coord for ring in poly][0]
    lat, lng = ring[0],ring[1]
    if lat is None or lng is None:
        print (f"no{i} feature is null")
        continue
    else:
        valid_feature.append(feature)

data["features"] = valid_feature

with open("/Users/xy/Documents/workspace/widget-spilhaus/cleaned-geojson.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent= 2)
    


