"""

trafficstatepoin The spatial dimension is one-dimensional datasets (i.e. point-based/segment-based/area-based datasets)

The processed files are stored in ./USTP_Model
File format after alignment, filtering and preprocessing:
    event dataset
   .geo：geo_id,type,coordinates
   .grid：dyna_id,type,time,row_id,column_id,flow
   .rel：rel_id,type,origin_id,destination_id,cost

"""
from tqdm import tqdm
import pandas as pd
import numpy as np
from datetime import datetime
from datetime import timedelta
from shapely import wkt
from tqdm import tqdm
import geopandas as gpd
import pandas as pd
import folium
import re
from shapely.geometry import MultiPolygon
import numpy as np
from shapely.geometry import Point

dataframe2 = gpd.read_file('../UrbanKG_data/Meta_data/CHI/Administrative_data/Area/Area.shp')
# Convert to latitude-longitude coordinate system
dataframe2 = dataframe2.to_crs('EPSG:4326')
seleceted_colums2 = ['area_numbe', 'community', 'geometry']
area_dataframe = dataframe2[seleceted_colums2]


"""

USTP_data 4: crime

"""
##################################################################################################
##################################################################################################

crime_dataframe = pd.read_csv('./Processed_data/CHI/CHI_crime.csv')
crime_dataframe['time'] = pd.to_datetime(crime_dataframe['time'], format="%m/%d/%Y %I:%M:%S %p")
crime_dataframe['time'] = crime_dataframe['time'].dt.strftime("%Y-%m-%d %H:%M:%S")
crime_numpy = crime_dataframe[['time', 'area_id']].values

begin_time = '2021-01-01 00:00:00'
format_pattern = '%Y-%m-%d %H:%M:%S'

crime_flow = np.zeros([4380, 77])

for i in range(crime_numpy.shape[0]):
    time_spannn_out = datetime.strptime(str(crime_numpy[i][0]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_out = int(time_spannn_out.total_seconds())
    time_step_out =  int(total_seconds_out / 7200)
    if 0<= time_step_out <= 4380 :
        crime_flow[time_step_out][ int(crime_numpy[i][1]) -1 ] = 1

now = datetime.strptime(begin_time, format_pattern)

NYCTaxi20200406_dyna = []
NYCTaxi20200406_dyna.append('dyna_id,type,time,entity_id,flow')
NYCTaxi20200406_geo = []
NYCTaxi20200406_geo.append('geo_id,type,coordinates')

dyna_id = 0
type = 'state'

for i in tqdm(range(crime_flow.shape[1])):
    for j in range(crime_flow.shape[0]):
        time_origin = now + timedelta(minutes=120 * j)
        time_write = time_origin.strftime('%Y-%m-%dT%H:%M:%SZ')
        flow = crime_flow[j][i]

        grid_record = str(dyna_id) + ',' + type + ',' + str(time_write) + ',' + str(i+1) + ',' + str(int(flow))
        dyna_id += 1
        NYCTaxi20200406_dyna.append(grid_record)

    geo_record = str(i+1) + ',' + 'Point' + ',"[]"'
    NYCTaxi20200406_geo.append(geo_record)

with open(r'./USTP/CHI/CHICrime20210112/CHICrime20210112.dyna','w') as f1:
    for i in range(len(NYCTaxi20200406_dyna)):
        f1.write(NYCTaxi20200406_dyna[i])
        f1.write('\n')
f1.close()

with open(r'./USTP/CHI/CHICrime20210112/CHICrime20210112.geo','w') as f1:
    for i in range(len(NYCTaxi20200406_geo)):
        f1.write(NYCTaxi20200406_geo[i])
        f1.write('\n')
f1.close()

NYCTaxi20200406_rel = []
NYCTaxi20200406_rel.append('rel_id,type,origin_id,destination_id,cost')

rel_id = 0
type = 'geo'
for i in tqdm(range(area_dataframe.shape[0])):
    head_area = area_dataframe.iloc[i].geometry
    for j in range(area_dataframe.shape[0]):
        tail_area = area_dataframe.iloc[j].geometry
        distance = head_area.distance(tail_area)
        NYCTaxi20200406_rel.append(str(rel_id) + ',' +  type + ',' + str(area_dataframe.iloc[i].area_numbe) + ',' + str(area_dataframe.iloc[j].area_numbe)
                                   + ',' + str(distance))
        rel_id += 1

with open(r'./USTP/CHI/CHICrime20210112/CHICrime20210112.rel','w') as f1:
    for i in range(len(NYCTaxi20200406_rel)):
        f1.write(NYCTaxi20200406_rel[i])
        f1.write('\n')
f1.close()

##################################################################################################
##################################################################################################
"""

USTP_data 5: 311 service

"""
crime_dataframe = pd.read_csv('./Processed_data/CHI/CHI_311_service.csv')

crime_numpy = crime_dataframe[['time', 'area_id']].values

begin_time = '2021-01-01 00:00:00'
format_pattern = '%Y-%m-%d %H:%M:%S'

crime_flow = np.zeros([4380, 77])

for i in range(crime_numpy.shape[0]):
    time_spannn_out = datetime.strptime(str(crime_numpy[i][0]), format_pattern) - datetime.strptime(begin_time, format_pattern)
    total_seconds_out = int(time_spannn_out.total_seconds())
    time_step_out =  int(total_seconds_out / 7200)
    if 0<= time_step_out <= 4380 :
        crime_flow[time_step_out][ int(crime_numpy[i][1]) -1 ] = 1

now = datetime.strptime(begin_time, format_pattern)

NYCTaxi20200406_dyna = []
NYCTaxi20200406_dyna.append('dyna_id,type,time,entity_id,flow')
NYCTaxi20200406_geo = []
NYCTaxi20200406_geo.append('geo_id,type,coordinates')

dyna_id = 0
type = 'state'

for i in tqdm(range(crime_flow.shape[1])):
    for j in range(crime_flow.shape[0]):
        time_origin = now + timedelta(minutes=120 * j)
        time_write = time_origin.strftime('%Y-%m-%dT%H:%M:%SZ')
        flow = crime_flow[j][i]

        grid_record = str(dyna_id) + ',' + type + ',' + str(time_write) + ',' + str(i+1) + ',' + str(int(flow))
        dyna_id += 1
        NYCTaxi20200406_dyna.append(grid_record)

    geo_record = str(i+1) + ',' + 'Point' + ',"[]"'
    NYCTaxi20200406_geo.append(geo_record)

with open(r'./USTP/CHI/CHI311Service20210112/CHI311Service20210112.dyna','w') as f1:
    for i in range(len(NYCTaxi20200406_dyna)):
        f1.write(NYCTaxi20200406_dyna[i])
        f1.write('\n')
f1.close()

with open(r'./USTP/CHI/CHI311Service20210112/CHI311Service20210112.geo','w') as f1:
    for i in range(len(NYCTaxi20200406_geo)):
        f1.write(NYCTaxi20200406_geo[i])
        f1.write('\n')
f1.close()

NYCTaxi20200406_rel = []
NYCTaxi20200406_rel.append('rel_id,type,origin_id,destination_id,cost')

rel_id = 0
type = 'geo'
for i in tqdm(range(area_dataframe.shape[0])):
    head_area = area_dataframe.iloc[i].geometry
    for j in range(area_dataframe.shape[0]):
        tail_area = area_dataframe.iloc[j].geometry
        distance = head_area.distance(tail_area)
        NYCTaxi20200406_rel.append(str(rel_id) + ',' +  type + ',' + str(area_dataframe.iloc[i].area_numbe) + ',' + str(area_dataframe.iloc[j].area_numbe)
                                   + ',' + str(distance))
        rel_id += 1

with open(r'./USTP/CHI/CHI311Service20210112/CHI311Service20210112.rel','w') as f1:
    for i in range(len(NYCTaxi20200406_rel)):
        f1.write(NYCTaxi20200406_rel[i])
        f1.write('\n')
f1.close()