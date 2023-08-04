"""

The processed files are stored in ./processed_data
File format after alignment, filtering and preprocessing:
    borough.csv: borough_id, borough_name, borough_polygon
    area.csv: area_id, area_name, area_polygon
    poi.csv: poi_id, poi_name, poi_category, lat, lng, borough_id, area_id
    road.csv: road_id, road_name, road_category, from_junction, to_junction, road_polygon, lat, lng, borough_id, area_id
    junction.csv: junction_id, junction_catogory, lat, lng, borough_id, area_id

"""
from shapely import wkt
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import folium
import re
from shapely.geometry import MultiPolygon
import numpy as np
from shapely.geometry import Point
"""
    
    borough, area's multi-polygon latitude and longitude reading
    
"""

######################################
dataframe1 = gpd.read_file('./Meta_data/CHI/Administrative_data/Borough/Borough.shp')
# 转换为经纬度坐标系
dataframe1 = dataframe1.to_crs('EPSG:4326')
seleceted_colums1 = ['BoroCode', 'BoroName', 'geometry']
borough_dataframe = dataframe1[seleceted_colums1]
borough_dataframe.to_csv('./Processed_data/CHI/CHI_borough.csv')
######################################
dataframe2 = gpd.read_file('./Meta_data/CHI/Administrative_data/Area/Area.shp')
# 转换为经纬度坐标系
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]
## 过滤掉 1, 103, 104 区域因为他们在孤岛，或者特别小
area_dataframe.to_csv('./Processed_data/CHI/CHI_area.csv')
######################################

"""

    Align POI to borough, area, judge whether POI point is inside polygon or multipolygon

"""

poi_dataframe = pd.read_csv('./Meta_data/CHI/POI/poi_filter.csv')
poi_datanumpy = poi_dataframe[['lng', 'lat']].values

# borough, area 矩阵
poi_borough_area_id = np.full((poi_datanumpy.shape[0], 2), 999)

for i in tqdm(range(poi_datanumpy.shape[0])):
    poi_point = Point(poi_datanumpy[i][0], poi_datanumpy[i][1])
    ## 遍历 borough
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(poi_point):
            poi_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ## 遍历 area
    for k in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[k].geometry
        if area_polygon.contains(poi_point):
            poi_borough_area_id[i][1] = area_dataframe.iloc[k].area_numbe
            break

# Add to the dataframe as a new column and filter
poi_dataframe[['borough_id', 'area_id']] = poi_borough_area_id
poi_dataframe = poi_dataframe[(poi_dataframe['borough_id'] != 999)]
poi_dataframe = poi_dataframe[(poi_dataframe['area_id'] != 999)]

poi_dataframe.to_csv('./Processed_data/CHI/CHI_poi.csv')

######################################

"""

    The road is aligned to the borough, area, to determine whether the road is inside the Polygon, or a small part of the road is inside the Polygon

"""

road_dataframe = pd.read_csv('./Meta_data/CHI/RoadNetwork/road_filter.csv')
road_datanumpy = road_dataframe[['geometry']].values

# borough, area
road_borough_area_id = np.full((road_datanumpy.shape[0], 2), 999)
for i in tqdm(range(road_datanumpy.shape[0])):
    road_linestring = wkt.loads(str(road_datanumpy[i][0]))
    ##
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(road_linestring) or borough_polygon.touches(road_linestring):
            road_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ##
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(road_linestring) or area_polygon.touches(road_linestring):
            road_borough_area_id[i][1] = area_dataframe.iloc[j].area_numbe
            break

road_dataframe[['borough_id', 'area_id']] = road_borough_area_id
road_dataframe = road_dataframe[(road_dataframe['borough_id'] != 999)]
road_dataframe = road_dataframe[(road_dataframe['area_id'] != 999)]

road_dataframe.to_csv('./Processed_data/CHI/CHI_road.csv')

######################################
"""

    The junction is aligned to the borough, area, and it is judged whether the junction is inside the Polygon

"""
junction_dataframe = pd.read_csv('./Meta_data/CHI/RoadNetwork/node_filter.csv')
junction_datanumpy = junction_dataframe[['lat', 'lng']].values

# borough, area 矩阵
junction_borough_area_id = np.full((junction_datanumpy.shape[0], 2), 999)

for i in tqdm(range(junction_datanumpy.shape[0])):
    junction_point = Point(junction_datanumpy[i][0], junction_datanumpy[i][1])
    ##
    for j in range(borough_dataframe.shape[0]):
        borough_polygon = borough_dataframe.iloc[j].geometry
        if borough_polygon.contains(junction_point):
            junction_borough_area_id[i][0] = borough_dataframe.iloc[j].BoroCode
            break
    ##
    for k in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[k].geometry
        if area_polygon.contains(junction_point):
            junction_borough_area_id[i][1] = area_dataframe.iloc[k].area_numbe
            break

# Add to the dataframe as a new column and filter
junction_dataframe[['borough_id', 'area_id']] = junction_borough_area_id
junction_dataframe = junction_dataframe[ (junction_dataframe['borough_id'] != 999)]
junction_dataframe = junction_dataframe[ (junction_dataframe['area_id'] != 999)]

junction_dataframe.to_csv('./Processed_data/CHI/CHI_junction.csv')