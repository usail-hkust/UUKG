"""

The processed files are stored in ./processed_data
File format after alignment, filtering and preprocessing:
   taxi.csv：start_time, end_time, start_area_id, end_area_id
   bike.csv: start_time, end_time, start_area_id, end_area_Id, start_road_id, end_road_id
   crime.csv: event_time, event_area_id
   311_service.csv: event_time, event_area_id

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
import pyarrow.parquet as pq
from datetime import datetime
#####################################

dataframe2 = gpd.read_file('../UrbanKG_data/Meta_data/CHI/Administrative_data/Area/Area.shp')

dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]

##################################

"""

USTP_Model 1: taxi

"""

#####################################

taxi_dataframe = pd.read_csv(u'./Meta_data/CHI/Flow_taxi/Taxi_Trips_-_2019.csv')

# Traverse the area first, and assign each record to the area
taxi_dataframe['start_area_id'] = None
taxi_dataframe['end_area_id'] = None

# filter time
taxi_dataframe['Trip Start Timestamp'] = pd.to_datetime(taxi_dataframe['Trip Start Timestamp'] )
taxi_dataframe['Trip End Timestamp'] = pd.to_datetime(taxi_dataframe['Trip End Timestamp'] )
start_date = pd.to_datetime('2019-04-01')
end_date = pd.to_datetime('2019-06-30')
taxi_dataframe = taxi_dataframe[(taxi_dataframe['Trip Start Timestamp'] >= start_date) & (taxi_dataframe['Trip Start Timestamp'] <= end_date)]
taxi_dataframe = taxi_dataframe[(taxi_dataframe['Trip End Timestamp'] >= start_date) & (taxi_dataframe['Trip End Timestamp'] <= end_date)]

# area 对齐
for index, row in tqdm(taxi_dataframe.iterrows(), total=taxi_dataframe.shape[0]):
    start_point = Point(taxi_dataframe.loc[index, 'Pickup Centroid Longitude'], taxi_dataframe.loc[index, 'Pickup Centroid Latitude'])
    end_point = Point(taxi_dataframe.loc[index, 'Dropoff Centroid Longitude'], taxi_dataframe.loc[index, 'Dropoff Centroid Latitude'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(start_point):
            taxi_dataframe.at[index, 'start_area_id'] = area_dataframe.iloc[j].area_numbe
            break
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(end_point):
            taxi_dataframe.at[index, 'end_area_id'] = area_dataframe.iloc[j].area_numbe
            break

new_columns = ['start_time', 'end_time', 'start_area_id', 'end_area_id', 'start_lng', 'start_lat', 'end_lng', 'end_lat']
selected_columns = ['Trip Start Timestamp', 'Trip End Timestamp', 'start_area_id', 'end_area_id',
                    'Pickup Centroid Longitude', 'Pickup Centroid Latitude', 'Dropoff Centroid Longitude', 'Dropoff Centroid Latitude']
taxi_filterframe = taxi_dataframe.loc[:, selected_columns]
taxi_filterframe.columns = new_columns
taxi_filterframe = taxi_filterframe[taxi_filterframe['start_area_id'].notna()]
taxi_filterframe = taxi_filterframe[taxi_filterframe['end_area_id'].notna()]
taxi_filterframe.to_csv('./Processed_data/CHI/CHI_taxi.csv')

##################################

"""

USTP_Model 2: bike

"""

#####################################

bike_dataframe = pd.read_csv(u'./Meta_data/CHI/Flow_bike/Divvy_Trips.csv')


bike_dataframe['start_area_id'] = None
bike_dataframe['end_area_id'] = None

#
bike_dataframe['START TIME'] = pd.to_datetime(bike_dataframe['START TIME'] )
bike_dataframe['STOP TIME'] = pd.to_datetime(bike_dataframe['STOP TIME'] )
start_date = pd.to_datetime('2019-04-01')
end_date = pd.to_datetime('2019-06-30')
bike_dataframe = bike_dataframe[(bike_dataframe['START TIME'] >= start_date) & (bike_dataframe['START TIME'] <= end_date)]
bike_dataframe = bike_dataframe[(bike_dataframe['STOP TIME'] >= start_date) & (bike_dataframe['STOP TIME'] <= end_date)]

# area
for index, row in tqdm(bike_dataframe.iterrows(), total=bike_dataframe.shape[0]):
    start_point = Point(bike_dataframe.loc[index, 'FROM LONGITUDE'], bike_dataframe.loc[index, 'FROM LATITUDE'])
    end_point = Point(bike_dataframe.loc[index, 'TO LONGITUDE'], bike_dataframe.loc[index, 'TO LATITUDE'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(start_point):
            bike_dataframe.at[index, 'start_area_id'] = area_dataframe.iloc[j].area_numbe
            break
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(end_point):
            bike_dataframe.at[index, 'end_area_id'] = area_dataframe.iloc[j].area_numbe
            break

new_columns = ['start_time', 'end_time', 'start_area_id', 'end_area_id', 'start_lng', 'start_lat', 'end_lng', 'end_lat']
selected_columns = ['START TIME', 'STOP TIME', 'start_area_id', 'end_area_id',
                    'FROM LONGITUDE', 'FROM LATITUDE', 'TO LONGITUDE', 'TO LATITUDE']
bike_filterframe = bike_dataframe.loc[:, selected_columns]
bike_filterframe.columns = new_columns
bike_filterframe = bike_filterframe[bike_filterframe['start_area_id'].notna()]
bike_filterframe = bike_filterframe[bike_filterframe['end_area_id'].notna()]
bike_filterframe.to_csv('./Processed_data/CHI/CHI_bike.csv')

"""

USTP_Model 3: crime

"""

#####################################

crime_dataframe = pd.read_csv(u'./Meta_data/CHI/Event_crime/CHI_complaint_20210112.csv')

#
crime_dataframe['area_id'] = None

# area
for index, row in tqdm(crime_dataframe.iterrows(), total=crime_dataframe.shape[0]):
    crime_point = Point(crime_dataframe.loc[index, 'Longitude'], crime_dataframe.loc[index, 'Latitude'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(crime_point):
            crime_dataframe.at[index, 'area_id'] = area_dataframe.iloc[j].area_numbe
            break

new_columns = ['time', 'area_id', 'lng', 'lat']
selected_columns = ['Date', 'area_id', 'Longitude', 'Latitude']
crime_dataframe = crime_dataframe.loc[:, selected_columns]
crime_dataframe.columns = new_columns
crime_dataframe = crime_dataframe[crime_dataframe['area_id'].notna()]
crime_dataframe.to_csv('./Processed_data/CHI/CHI_crime.csv')


"""

USTP_Model 4: 311 service 

"""

service_dataframe = pd.read_csv(u'./Meta_data/CHI/Event_311/311_sercice_20210112.csv')

# First traverse the area and assign each record to the area
service_dataframe['area_id'] = None

# #
service_dataframe['CREATED_DATE'] = pd.to_datetime(service_dataframe['CREATED_DATE'] )
start_date = pd.to_datetime('2021-01-01')
end_date = pd.to_datetime('2021-12-31')
service_dataframe = service_dataframe[(service_dataframe['CREATED_DATE'] >= start_date) & (service_dataframe['CREATED_DATE'] <= end_date)]

# area
for index, row in tqdm(service_dataframe.iterrows(), total=service_dataframe.shape[0]):
    crime_point = Point(service_dataframe.loc[index, 'LONGITUDE'], service_dataframe.loc[index, 'LATITUDE'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(crime_point):
            service_dataframe.at[index, 'area_id'] = area_dataframe.iloc[j].area_numbe
            break

new_columns = ['time', 'area_id', 'lng', 'lat']
selected_columns = ['CREATED_DATE', 'area_id', 'LONGITUDE', 'LATITUDE']
service_dataframe = service_dataframe.loc[:, selected_columns]
service_dataframe.columns = new_columns
service_dataframe = service_dataframe[service_dataframe['area_id'].notna()]
service_dataframe.to_csv('./Processed_data/CHI/CHI_311_service.csv')