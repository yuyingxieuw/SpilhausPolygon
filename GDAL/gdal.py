from osgeo import gdal 
dataset = gdal.Open("/Users/xy/Documents/workspace/widget-spilhaus/GDAL/Map8.12.tif")
print(f"Projection:{dataset.GetProjection()}")
print(f"Driver: {dataset.GetDriver().ShortName}, {dataset.GetDriver().LongName}")
print("Size: {} X {} X {}".format(dataset.RasterXSize, dataset.RasterYSize, dataset.RasterCount))
print("GeoTransform:", dataset.GetGeoTransform())
