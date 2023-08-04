"""

The processed files are stored in ./UrbanKG
File format after alignment, filtering and preprocessing:

    entity2id.txt: entity, entity_id
    relation2id.txt: relation, relation_id
    triplets.txt：entity_id, relation_id, entity_id
    train.txt
    valid.txt
    test.txt

"""
import random
from tqdm import tqdm

def get_entity2id_relation2id(KG, entity2id, relation2id):
    entity = []
    relations = []
    with open(KG) as f:
        for line in f.readlines():
            temp = line.split()
            entity.append(temp[0])
            entity.append(temp[2])
            relations.append(temp[1])
    entity = list(set(entity))
    relations = list(set(relations))
    f.close()

    with open(entity2id,'w') as f2:
        for i in range(len(entity)):
            f2.write(entity[i] + ' ')
            f2.write(str(i))
            f2.write('\n')
        f2.close()


    with open(relation2id,'w') as f3:
        for j in range(len(relations)):
            f3.write(relations[j]+' ')
            f3.write(str(j))
            f3.write('\n')
        f3.close()

def produce_train_val_test(KG, entity2id, realtion2id, triple):
    h_r_t = []

    h = []
    r = []
    t = []
    with open(KG) as f:
        for line in f.readlines():
            temp = line.split()
            h.append(temp[0])
            t.append(temp[2])
            r.append(temp[1])

    entity_category_dict = {}
    relation_category_dict = {}
    with open(entity2id) as f:
        for line in f.readlines():
            temp = line.split()
            entity_category_dict.update({temp[0] : temp[1]})
    with open(realtion2id) as f1:
        for line in f1.readlines():
            temp1 = line.split()
            relation_category_dict.update({temp1[0] : temp1[1]})

    with open(triple, 'w') as f2:
        for i in tqdm(range(len(h))):
            f2.write(str(entity_category_dict[h[i]]) + ' ')
            f2.write(str(relation_category_dict[r[i]]) + ' ')
            f2.write(str(entity_category_dict[t[i]]))
            f2.write('\n')


def get_train_val_test(triple, train_address, valid_address, test_address):
    h_r_t = []
    with open(triple) as f:
        for line in f.readlines():
            temp = line.split()
            h_r_t.append(temp)
    random.shuffle(h_r_t)
    train = int(len(h_r_t) * 0.9)
    valid = int(len(h_r_t) * 0.05)
    test = len(h_r_t) - train - valid

    with open(train_address, 'w') as f:
        for i in range(train):
            f.write(h_r_t[i][0] + '\t')
            f.write(h_r_t[i][1] + '\t')
            f.write(h_r_t[i][2])
            f.write('\n')
    f.close()

    with open(valid_address, 'w') as f:
        for i in range(valid):
            f.write(h_r_t[train + i][0] + '\t')
            f.write(h_r_t[train + i][1] + '\t')
            f.write(h_r_t[train + i][2])
            f.write('\n')
    f.close()

    with open(test_address, 'w') as f:
        for i in range(test):
            f.write(h_r_t[train + valid + i][0] + '\t')
            f.write(h_r_t[train + valid + i][1] + '\t')
            f.write(h_r_t[train + valid + i][2])
            f.write('\n')
    f.close()



if __name__ == "__main__":
    KG_NYC = "./UrbanKG/NYC/UrbanKG_NYC.txt"
    entity2id_NYC = "./UrbanKG/NYC/entity2id_NYC.txt"
    relation2id_NYC = "./UrbanKG/NYC/relation2id_NYC.txt"
    triple_NYC = "./UrbanKG/NYC/triplets_NYC.txt"
    train_NYC = './UrbanKG/NYC/train_NYC.txt'
    valid_NYC = './UrbanKG/NYC/valid_NYC.txt'
    test_NYC = './UrbanKG/NYC/test_NYC.txt'

    get_entity2id_relation2id(KG_NYC, entity2id_NYC, relation2id_NYC)
    produce_train_val_test(KG_NYC, entity2id_NYC, relation2id_NYC, triple_NYC)
    get_train_val_test(triple_NYC, train_NYC, valid_NYC, test_NYC)


    KG_CHI = "./UrbanKG/CHI/UrbanKG_CHI.txt"
    entity2id_CHI = "./UrbanKG/CHI/entity2id_CHI.txt"
    relation2id_CHI = "./UrbanKG/CHI/relation2id_CHI.txt"
    triple_CHI = "./UrbanKG/CHI/triplets_CHI.txt"
    train_CHI = './UrbanKG/CHI/train_CHI.txt'
    valid_CHI = './UrbanKG/CHI/valid_CHI.txt'
    test_CHI = './UrbanKG/CHI/test_CHI.txt'

    get_entity2id_relation2id(KG_CHI, entity2id_CHI, relation2id_CHI)
    produce_train_val_test(KG_CHI, entity2id_CHI, relation2id_CHI, triple_CHI)
    get_train_val_test(triple_CHI, train_CHI, valid_CHI, test_CHI)

    # Extract the KG_id of the required entiy
    # with open("/home/ningyansong/UrbanKG/KDD_data_prepare/NYC/entity2id_NYC_GUrbanKG.txt") as f:
    #     crime_entity = []
    #     for line in f.readlines():
    #         if 'region/' in line:
    #             # print(line)
    #             crime_entity.append(line)
    # print(len(crime_entity))
    # with open('NYC_poi_KGid', 'w') as f:
    #     for i in range(len(crime_entity)):
    #         f.write(crime_entity[i])

