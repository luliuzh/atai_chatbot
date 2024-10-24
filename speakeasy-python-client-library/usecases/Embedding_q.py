import json
import spacy
import csv
import numpy as np
import os
import rdflib
import pandas as pd
from sklearn.metrics import pairwise_distances

# 定义命名空间
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

# 加载图数据
graph = rdflib.Graph().parse(r'D:\dev\python\python-learn\ATAI\speakeasy-python-client-library\14_graph.nt', format='turtle')




def get_closest_entity(entity_label, relation_label):
    # 获取实体对应的 ID
    # 加载嵌入向量
    entity_emb = np.load(r'D:\dev\python\python-learn\ATAI\entity_embeds.npy')
    relation_emb = np.load(r'D:\dev\python\python-learn\ATAI\relation_embeds.npy')

    # 加载实体和关系字典
    with open(r'D:\dev\python\python-learn\ATAI\entity_ids.del', 'r') as ifile:
        ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
        id2ent = {v: k for k, v in ent2id.items()}

    with open(r'D:\dev\python\python-learn\ATAI\relation_ids.del', 'r') as ifile:
        rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
        id2rel = {v: k for k, v in rel2id.items()}

    ent2lbl = {ent: str(lbl) for ent, lbl in graph.subject_objects(RDFS.label)}
    lbl2ent = {lbl: ent for ent, lbl in ent2lbl.items()}
    entity = lbl2ent.get(entity_label)

    with open(r'D:\dev\python\python-learn\ATAI\speakeasy-python-client-library\usecases\data.json', 'r') as json_file:
        loaded_relation_data = json.load(json_file)

    # 获取关系的 WDT.Pxxx 格式的键
    relation_key = next((key for key, value in loaded_relation_data.items() if value == relation_label), None)

    if relation_key is None:
        return None  # 如果没有找到关系

    # 生成关系的 URI
    relation_uri = WDT[relation_key]

    # 获取实体的向量
    head = entity_emb[ent2id[entity]]
    # 获取关系的向量
    pred = relation_emb[rel2id[relation_uri]]

    # 根据 TransE 评分函数添加向量
    lhs = head + pred
    # 计算与任何实体的距离
    dist = pairwise_distances(lhs.reshape(1, -1), entity_emb).reshape(-1)
    # 找到最可能的实体
    most_likely = dist.argsort()

    # 返回与 ID 对应的 label
    closest_entity_id = most_likely[0]  # 取最接近的结果
    closest_entity_uri = id2ent[closest_entity_id]  # 获取对应的 URI

    # 使用 ent2lbl 获取 URI 对应的 label
    closest_entity_label = ent2lbl.get(closest_entity_uri, "Unknown Label")

    return closest_entity_label  # 返回 label

# 示例调用
result = get_closest_entity('Weathering with You', 'MPAA film rating')
print(f"Closest entity label: {result}")  # 打印返回的 label
result = get_closest_entity('Good Neighbors', 'genre')
print(f"Closest entity label: {result}")  # 打印返回的 label
result = get_closest_entity('The Masked Gang: Cyprus', 'screenwriter')
print(f"Closest entity label: {result}")  # 打印返回的 label