from factual_q import Query_Processer
from graph_kg import graph

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
    print(f'query:{query}')
    # entity = my_query_processer.entity_extractor(query)
    entity = my_query_processer.entity_extractor(query)
    relation = my_query_processer.relation_extractor(query)
    print(f"entity:{entity}")
    print(f"ralation:{relation}'\n")

# entity: list, relation: dict
for entity_item, relation_item in zip(entity, relation.values()):
    entity_value = list(entity_item.values())[0]
    relation_value = relation_item
    result = my_query_processer.query_knowledge_graph(entity=entity_value, relation=relation_value)
    print(result)

    

