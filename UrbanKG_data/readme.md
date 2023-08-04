### Guidance on data usage and processing

We store the original unprocessed files in the **'./Meta_data'** directory. To preprocess, align, and filter these files, we utilize either the **`preprocess_meta_data_nyc.py`** or **`preprocess_meta_data_chi.py`** script. The processed data is then saved in the **'./Processed_data'** directory. Finally, we execute the **`construct_UrbanKG_NYC.py`** or **`construct_UrbanKG_CHI.py`** script to obtain the constructed urban knowledge graphs, which are stored in the **'./UrbanKG'** directory.

We divide the training set, verification set and test set by **`train_val_test_ent2id_rel2id.py`**

The file information in each directory is as follows:

```
./Meta_data    Raw data set: administrative division data, POI and road network data
./Processed_data   Aligned datasets: administrative region entity, POI entity, road network entity
./UrbanKG    City fact triples obtained from 8 entities and 13 relationships
```

The following types of atomic files are defined:

| filename            | content                                 | example              |
| ------------------- | --------------------------------------- | -------------------- |
| entity2id_XXX.txt   | entity_name, entity_id                  | Road/106710 11       |
| relation2id_XXX.txt | relation_name, relation_id              | BNB 2                |
| train               | entity_id, relation_id, entity_id       | 196632  12 85987     |
| valid               | entity_id, relation_id, entity_id       | 43982   10 233474    |
| test                | entity_id, relation_id, entity_id       | 167134  6  75149     |
| triplet.txt         | entity_id, relation_id, entity_id       | 48034   12 168303    |
| UrbanKG_XXX.txt     | entity_name, relation_name, entity_name | POI/663 PLA Area/230 |

### To create your urban knowledge graph dataset
Our urban knowledge graph construction scheme is highly reusable. You can prepare your urban data following either the file format in **'./Meta_data'** or **'./Processed_data'**, and then run scripts **`construct_UrbanKG_XXX.py`** to build your personalized urban knowledge graph. This flexibility allows you to adapt the construction process to various cities and datasets easily.

### Visualization
<img src="https://github.com/usail-hkust/UUKG/blob/main/UrbanKG_data/visualization.png" width="440px">

We offer comprehensive visualization solutions for all types of urban knowledge. By leveraging the powerful visualization capabilities of **Folium**, we provide an intuitive understanding of the urban entities and relationships encoded in the constructed urban knowledge map. This allows users to interact with and explore the urban knowledge graph in a user-friendly manner, facilitating better insights and analysis of the urban data.

You can run **`UrbanKG_visulization_XXX.py`** to get the overall visualization of urban entities like borough, area, POI and road segment. You can also develop other visualization function according to your preferences.
