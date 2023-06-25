<div align="center">
    <img src="https://github.com/usail-hkust/UUKG/blob/main/title.png" width="440px">
    <p> <b>
        The Unified Urban Knowledge Graph Dataset for Urban Spatiotemporal Prediction.</b>
    </p>

------

<p align="center">
  <a href="#overview">Overview</a> •
  <a href="#installation">Installation</a> •
  <a href="#how-to-run">Data & Model</a> •
  <a href="#other-kg-representation-open-source-projects">Others</a> 
</p>
</div>

## Overview
UUKG is an open-sourced and multifaceted urban knowledge graph dataset compatible with various USTP tasks. As the original dataset is quite large, we have included example data, data processing code, and model code to assist readers in understanding our research. The complete data sources can be found on [Google Drive](https://drive.google.com/drive/folders/1egTmnKRzTQuyW_hsbFURUonGC-bJmBHW?usp=sharing).

## Installation

Enter the task directory and install library
```bash
cd UUKG/UrbanKG_Embedding_Model
pip install -r requirements.txt
cd UUKG/USTP_Model
pip install -r requirements.txt
```

## Data & Model

The expected structure of files is:

```
UUKG
 |-- UrbanKG_data  # UrbanKG_data
 |    |-- Meta_data
 |    |    |-- NYC  # meta data for New York
 |    |    |    |-- Administrative_data    
 |    |    |    |-- POI     
 |    |    |    |-- RoadNetwork     
 |    |    |-- CHI  # meta data for Chicago
 |    |    |    |-- Administrative_data    
 |    |    |    |-- POI     
 |    |    |    |-- RoadNetwork     
 |    |-- Processed_data  # 
 |    |    |-- NYC
 |    |    |-- CHI 
 |    |-- UrbanKG  # constructed urban knowledge graph
 |    |    |-- NYC
 |    |    |    |-- entity2id_NYC.txt   
 |    |    |    |-- relation2id_NYC.txt     
 |    |    |    |-- UrbanKG_NYC.txt
 |    |    |    |-- triplets_NYC.txt   
 |    |    |    |-- train_NYC.txt  
 |    |    |    |-- valid_NYC.txt
 |    |    |    |-- test_NYC.txt
 |    |    |-- CHI 
 |    |-- construct_UrbanKG_NYC.py # UrbanKG constructuion
 |    |-- preprocess_meta_data_nyc.py # data preprocessing
 |-- UrbanKG_Embedding_Model  # KG embedding
 |    |-- data
 |    |    |-- NYC
 |    |    |-- CHI 
 |    |-- dataset
 |    |-- models
 |    |-- optimizer
 |    |-- utils
 |    |-- run.py # KG embedding 
 |    |-- requirements.txt
 |-- USTP_data  # USTP_data
 |    |-- Meta_data
 |    |    |-- NYC  # meta data for New York
 |    |    |    |-- Flow_taxi    
 |    |    |    |-- Flow_bike     
 |    |    |    |-- Flow_human     
 |    |    |    |-- Event_crime     
 |    |    |    |-- Event_311  
 |    |    |-- CHI  # meta data for Chicago
 |    |-- Processed_data  # 
 |    |    |-- NYC
 |    |    |-- CHI 
 |    |-- USTP  # constructed urban spatiotemporal prediction dataset
 |    |    |-- NYC
 |    |    |    |-- NYCTaxi20200406  
 |    |    |    |-- NYCBike20200406     
 |    |    |    |-- NYCHuman20200406
 |    |    |    |-- NYCCrime20210112   
 |    |    |    |-- NYC311Service20210112  
 |    |    |-- CHI 
 |    |-- utils  # constructed urban spatiotemporal prediction dataset
 |    |-- preprocess_meta_data_nyc # USTP data preprocessing
 |    |-- construct_USTP_Pointflow_NYC.py # USTP flow dataset construction
 |    |-- construct_USTP_Event_NYC.py # USTP event dataset construction
 |-- USTP_Model  # USTP_model
 |    |-- libcity
 |    |-- log
 |    |-- raw_data
 |    |-- run.py # urban spatiotemporal prediction 
 |    |-- requirements.txt
 |-- README.md

```

## Reference
If you find the code useful for your research, please consider citing
```bash
@article{ning2023uukg,
  title={UUKG: Unified Urban Knowledge Graph Dataset for Urban Spatiotemporal Prediction},
  author={Ning, Yansong and Liu, Hao and Wang, Hao and Zeng, Zhenyu and Xiong, Hui},
  journal={arXiv preprint arXiv:2306.11443},
  year={2023}
}
```
