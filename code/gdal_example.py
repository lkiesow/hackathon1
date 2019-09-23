import gdal
import numpy
import geojson
import geojsonio

# Path of netCDF file
# note: this data file is not in the repo, it was retrieved from:
# https://data.lkiesow.io/emissions-api/
FILE_NAME = "data/S5P_NRTI_L2__CO_____20190921T104303_20190921T104803_10045_01_010302_20190921T124803.nc"

# Specify the layer name to read
LAYER_NAME = '//PRODUCT/carbonmonoxide_total_column'
LONGITUDE_NAME = '//PRODUCT/longitude'
LATITUDE_NAME = '//PRODUCT/latitude'
QA_VALUE_NAME = '//PRODUCT/qa_value'


def convert_to_point(lat, lon, index):
    return (geojson.Point((float(lon[index]), float(lat[index]))))


def main():
    ds = gdal.Open(f'HDF5:{FILE_NAME}:{LAYER_NAME}')
    data = numpy.ndarray.flatten(ds.ReadAsArray())

    ds = gdal.Open(f'HDF5:{FILE_NAME}:{LONGITUDE_NAME}')
    lon = numpy.ndarray.flatten(ds.ReadAsArray())

    ds = gdal.Open(f'HDF5:{FILE_NAME}:{LATITUDE_NAME}')
    lat = numpy.ndarray.flatten(ds.ReadAsArray())

    ds = gdal.Open(f'HDF5:{FILE_NAME}:{QA_VALUE_NAME}')
    qa = numpy.ndarray.flatten(ds.ReadAsArray())

    features = []
    for i in range(0, 10000):
        if qa[i] < 50:
            continue
        value = float(data[i])
        point = convert_to_point(lat, lon, i)
        properties = {
                'carbonmonoxide': value
                }
        features.append(geojson.Feature(geometry=point, properties=properties))
    feature_collection = geojson.FeatureCollection(features)
    dump = geojson.dumps(feature_collection, sort_keys=True)

    # Cannot handle a large number (1000) of points
    #geojsonio.display(dump)
    print(dump)


if __name__ == '__main__':
    main()
