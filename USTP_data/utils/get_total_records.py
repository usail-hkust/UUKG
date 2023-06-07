"""

Number of records per dataset

"""
import pandas as pd

NYC_Taxi = pd.read_csv('../Processed_data/NYC/NYC_taxi.csv')
print("NYC_Taxi records: ", len(NYC_Taxi))

NYC_Bike = pd.read_csv('../Processed_data/NYC/NYC_bike_road.csv')
print("NYC_Bike records: ", len(NYC_Bike))

NYC_Human = pd.read_csv('../Processed_data/NYC/NYC_human.csv')
print("NYC_Human records: ", len(NYC_Human))

NYC_Crime = pd.read_csv('../Processed_data/NYC/NYC_crime.csv')
print("NYC_Crime records: ", len(NYC_Crime))

NYC_311_service = pd.read_csv('../Processed_data/NYC/NYC_311_service.csv')
print("NYC_311_service records: ", len(NYC_311_service))

CHI_Taxi = pd.read_csv('../Processed_data/CHI/CHI_taxi.csv')
print("CHI_Taxi records: ", len(CHI_Taxi))

CHI_Bike = pd.read_csv('../Processed_data/CHI/CHI_bike.csv')
print("CHI_Bike records: ", len(CHI_Bike))

CHI_Human = pd.read_csv('../Processed_data/CHI/CHI_human.csv')
print("CHI_Human records: ", len(CHI_Human))

CHI_Crime = pd.read_csv('../Processed_data/CHI/CHI_crime.csv')
print("CHI_Crime records: ", len(CHI_Crime))

CHI_311_service = pd.read_csv('../Processed_data/CHI/CHI_311_service.csv')
print("CHI_311_service records: ", len(CHI_311_service))
