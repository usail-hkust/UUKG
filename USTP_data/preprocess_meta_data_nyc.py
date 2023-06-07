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

dataframe2 = gpd.read_file('../UrbanKG_data/Meta_data/NYC/Administrative_data/Area/Area.shp')

dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['OBJECTID', 'zone', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]

area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 1]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 103]
area_dataframe = area_dataframe[area_dataframe['OBJECTID'] != 104]

##################################

"""

USTP_Model 1: taxi

"""

#####################################

taxidata_2020_04 = pq.read_table(u'./Meta_data/NYC/Flow_taxi/yellow_tripdata_2020-04.parquet').to_pandas()
taxidata_2020_05 = pq.read_table(u'./Meta_data/NYC/Flow_taxi/yellow_tripdata_2020-05.parquet').to_pandas()
taxidata_2020_06 = pq.read_table(u'./Meta_data/NYC/Flow_taxi/yellow_tripdata_2020-06.parquet').to_pandas()

taxi_dataframe = pd.concat([taxidata_2020_04, taxidata_2020_05, taxidata_2020_06], ignore_index=True)


taxi_dataframe = taxi_dataframe[taxi_dataframe['PULocationID'] != 1]
taxi_dataframe = taxi_dataframe[taxi_dataframe['PULocationID'] != 103]
taxi_dataframe = taxi_dataframe[taxi_dataframe['PULocationID'] != 104]
taxi_dataframe = taxi_dataframe[taxi_dataframe['DOLocationID'] != 1]
taxi_dataframe = taxi_dataframe[taxi_dataframe['DOLocationID'] != 103]
taxi_dataframe = taxi_dataframe[taxi_dataframe['DOLocationID'] != 104]
taxi_dataframe = taxi_dataframe[taxi_dataframe['PULocationID'] <= 263]
taxi_dataframe = taxi_dataframe[taxi_dataframe['DOLocationID'] <= 263]

new_columns = ['start_time', 'end_time', 'start_area_id', 'end_area_id']
selected_columns = ['tpep_pickup_datetime', 'tpep_dropoff_datetime', 'PULocationID', 'DOLocationID']
taxi_filterframe = taxi_dataframe.loc[:, selected_columns]
taxi_filterframe.columns = new_columns
taxi_filterframe.to_csv('./Processed_data/NYC/NYC_taxi.csv')

#####################################

"""

USTP_Model 2: bike

"""
bikedata_2020_04 = pd.read_csv(u'./Meta_data/NYC/Flow_bike/202004-citibike-tripdata.csv')
bikedata_2020_05 = pd.read_csv(u'./Meta_data/NYC/Flow_bike/202005-citibike-tripdata.csv')
bikedata_2020_06 = pd.read_csv(u'./Meta_data/NYC/Flow_bike/202006-citibike-tripdata.csv')

bike_dataframe = pd.concat([bikedata_2020_04, bikedata_2020_05, bikedata_2020_06], ignore_index=True)


bike_dataframe['start_area_id'] = None
bike_dataframe['end_area_id'] = None

for index, row in tqdm(bike_dataframe.iterrows(), total=bike_dataframe.shape[0]):
    start_point = Point(bike_dataframe.loc[index, 'start station longitude'], bike_dataframe.loc[index, 'start station latitude'])
    end_point = Point(bike_dataframe.loc[index, 'end station longitude'], bike_dataframe.loc[index, 'end station latitude'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(start_point):
            bike_dataframe.at[index, 'start_area_id'] = area_dataframe.iloc[j].OBJECTID
            break
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(end_point):
            bike_dataframe.at[index, 'end_area_id'] = area_dataframe.iloc[j].OBJECTID
            break

new_columns = ['start_time', 'end_time', 'start_area_id', 'end_area_id', 'start_lng', 'start_lat', 'end_lng', 'end_lat']
selected_columns = ['starttime', 'stoptime', 'start_area_id', 'end_area_id',
                    'start station longitude', 'start station latitude', 'end station longitude', 'end station latitude']
bike_filterframe = bike_dataframe.loc[:, selected_columns]
bike_filterframe.columns = new_columns
bike_filterframe = bike_filterframe[bike_filterframe['start_area_id'].notna()]
bike_filterframe = bike_filterframe[bike_filterframe['end_area_id'].notna()]
bike_filterframe.to_csv('./Processed_data/NYC/NYC_bike.csv')


"""

USTP_Model 3:crime

"""

crime_dataframe = pd.read_csv(u'./Meta_data/NYC/Event_crime/NYPD_complaint_20210112.csv')


crime_dataframe['area_id'] = None


for index, row in tqdm(crime_dataframe.iterrows(), total=crime_dataframe.shape[0]):
    crime_point = Point(crime_dataframe.loc[index, 'Longitude'], crime_dataframe.loc[index, 'Latitude'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(crime_point):
            crime_dataframe.at[index, 'area_id'] = area_dataframe.iloc[j].OBJECTID
            break

new_columns = ['time', 'area_id', 'lng', 'lat']
selected_columns = ['Date', 'area_id', 'Longitude', 'Latitude']
crime_dataframe = crime_dataframe.loc[:, selected_columns]
crime_dataframe.columns = new_columns
crime_dataframe = crime_dataframe[crime_dataframe['area_id'].notna()]
crime_dataframe.to_csv('./Processed_data/NYC/NYC_crime.csv')

"""

USTP_Model 4: 311 service 

"""

service_dataframe = pd.read_csv(u'./Meta_data/NYC/Event_311/311_sercice_20210112.csv')


service_dataframe['area_id'] = None


for index, row in tqdm(service_dataframe.iterrows(), total=service_dataframe.shape[0]):
    crime_point = Point(service_dataframe.loc[index, 'Longitude'], service_dataframe.loc[index, 'Latitude'])
    for j in range(area_dataframe.shape[0]):
        area_polygon = area_dataframe.iloc[j].geometry
        if area_polygon.contains(crime_point):
            service_dataframe.at[index, 'area_id'] = area_dataframe.iloc[j].OBJECTID
            break

new_columns = ['time', 'area_id', 'lng', 'lat']
selected_columns = ['Time', 'area_id', 'Longitude', 'Latitude']
service_dataframe = service_dataframe.loc[:, selected_columns]
service_dataframe.columns = new_columns
service_dataframe = service_dataframe[service_dataframe['area_id'].notna()]
service_dataframe.to_csv('./Processed_data/NYC/NYC_311_service.csv')