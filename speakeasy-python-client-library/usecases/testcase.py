from factual_q import Query_Processer

my_query_processer = Query_Processer()
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
    entity = my_query_processer.entity_extractor(query)
    relation = my_query_processer.relation_extractor(query)
    print(f"entity:{entity}")
    print(f"ralation:{relation}'\n")
# sample use
# query = 'Who is the director of Star Wars: Episode VI - Return of the Jedi? '
# entity = my_query_processer.entity_extractor(query)
# relation = my_query_processer.relation_extractor(query)
# print(entity)
# print(relation)

# query = 'Who is the screenwriter of The Masked Gang: Cyprus? '
# entity = my_query_processer.entity_extractor(query)
# relation = my_query_processer.relation_extractor(query)
# print(entity)
# print(relation)

# query = "What is the MPAA film rating of Weathering with You? "
# entity = my_query_processer.entity_extractor(query)
# relation = my_query_processer.relation_extractor(query)
# print(entity)
# print(relation)

# query = "What is the genre of Good Neighbors? "
# entity = my_query_processer.entity_extractor(query)
# relation = my_query_processer.relation_extractor(query)
# print(entity)
# print(relation)


