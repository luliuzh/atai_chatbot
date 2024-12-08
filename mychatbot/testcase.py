from factual_q import Query_Processer
import rdflib
from  Embedding_q import get_closest_entity
import pandas as pd
from sklearn.metrics import pairwise_distances
from graph import graph

my_graph = graph
my_query_processer = Query_Processer(my_graph)
queries = [
    # 'Who is the director of Good Will Hunting? ',
    # 'Who directed The Bridge on the River Kwai? ',
    # 'Who is the director of Star Wars: Episode VI - Return of the Jedi?',
    # 'Who is the screenwriter of The Masked Gang: Cyprus? ',
    # 'What is the MPAA film rating of Weathering with You? ',
    # 'What is the genre of Good Neighbors? ',
    # 'When was "The Godfather" released?',
    

    'Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?',
    'Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.'
]


for query in queries:
    print(f'query: {query}')

    # 提取实体和关系
    # entity = my_query_processer.entity_extractor(query)
    entities = my_query_processer.entity_extractor_recommender(query)
    # relation = my_query_processer.relation_extractor(query, entity)

    print(f"entity: {entities}\n")
    '''
    query: Given that I like The Lion King, Pocahontas, and The Beauty and the Beast, can you recommend some movies?
    entity: [{'Q134138': 'The Lion King'}, {'Q27688562': 'Pocahontas'}, {'Q17508441': 'Beauty and the Beast'}]

    query: Recommend movies like Nightmare on Elm Street, Friday the 13th, and Halloween.
    entity: [{'Q300508': 'A Nightmare on Elm Street'}, {'Q1454815': 'Friday the 13th'}, {'Q20666646': 'Halloween'}]
    '''

    # print(f"relation: {relation}\n")

    # # 针对每个实体和关系，查询知识图谱
    # for entity_item, relation_item in zip(entity, relation.values()):
    #     entity_value = list(entity_item.values())[0]
    #     relation_value = relation_item

    #     # 调用 get_closest_entity 函数并存储结果
    #     result = get_closest_entity(graph, entity_label=entity_value, relation_label=relation_value)
    #     if result == None :
    #         print ()
    #     # 输出结果
    #     print(f"Closest entity for {entity_value} with relation {relation_value}: {result}")


    

