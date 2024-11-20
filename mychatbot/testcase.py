from factual_q import Query_Processer
import rdflib
from  Embedding_q import get_closest_entity
import pandas as pd
from sklearn.metrics import pairwise_distances

# 定义命名空间
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')


graph = rdflib.Graph().parse(r'mychatbot/data/14_graph.nt', format='turtle')
my_query_processer = Query_Processer(graph)
queries = [
    'Who is the director of Good Will Hunting? ',
    'Who directed The Bridge on the River Kwai? ',
    'Who is the director of Star Wars: Episode VI - Return of the Jedi?',
    'Who is the screenwriter of The Masked Gang: Cyprus? ',
    'What is the MPAA film rating of Weathering with You? ',
    'What is the genre of Good Neighbors? ',
    'When was "The Godfather" released?'
]


for query in queries:
    print(f'query: {query}')

    # 提取实体和关系
    entity = my_query_processer.entity_extractor(query)
    relation = my_query_processer.relation_extractor(query, entity)

    print(f"entity: {entity}")
    print(f"relation: {relation}\n")

    # 针对每个实体和关系，查询知识图谱
    for entity_item, relation_item in zip(entity, relation.values()):
        entity_value = list(entity_item.values())[0]
        relation_value = relation_item

        # 调用 get_closest_entity 函数并存储结果
        result = get_closest_entity(graph, entity_label=entity_value, relation_label=relation_value)
        if result == None :
            print ()
        # 输出结果
        print(f"Closest entity for {entity_value} with relation {relation_value}: {result}")


    

