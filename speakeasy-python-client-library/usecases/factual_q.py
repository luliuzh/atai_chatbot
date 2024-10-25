from transformers import AutoTokenizer
from transformers import pipeline
import spacy
import json
from fuzzywuzzy import fuzz
from fuzzywuzzy import process
import json
import rdflib
import csv
import re

# step1: extract entity and relation
class Query_Processer:
    def __init__(self, graph):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", 
                        tokenizer=self.tokenizer,
                        aggregation_strategy = "simple")
        
        with open('data_entity.json', 'r') as f:
            self.data_entities = json.load(f)
        self.graph = graph
        self.RDFS = rdflib.namespace.RDFS

    def query_knowledge_graph(self, entity: str, relation: str) -> str:
        # Step 1: Prepare the entity and relation by resolving their URIs
        # Assuming you have a way to map entity names and relation labels to URIs
        self.ent2lbl = {ent: str(lbl) for ent, lbl in self.graph.subject_objects(self.RDFS.label)}
        self.lbl2ent = {lbl: ent for ent, lbl in self.ent2lbl.items()}

        entity_uri = self.lbl2ent.get(entity)  # Example: Resolve 'Good Neighbors' to URI
        relation_uri = self.lbl2ent.get(relation)  # Example: Resolve 'genre' to URI

        if not entity_uri or not relation_uri:
            return "Entity or relation not found in the knowledge graph."
        
        # Step 2: Query the knowledge graph to retrieve objects related to the entity and relation
        results = []
        for obj in self.graph.objects(subject=entity_uri, predicate=relation_uri):
            results.append(str(obj))  # Convert the object to a string

        # Return the results in a readable format
        if results:
            return f"Results for '{entity}' with relation '{relation}': {', '.join(results)}"
        else:
            return f"No results found for '{entity}' with relation '{relation}'."

    def _entity2id(self, entity: str)-> dict:

        # 定义模糊匹配的阈值（例如 88 表示 88% 相似度）
        threshold = 88

        # 匹配结果存储
        matching_results = {}

        # 使用 fuzzywuzzy 提取与输入实体最相似的 entity_title
        best_match = process.extractOne(entity, self.data_entities.values(), scorer=fuzz.ratio, score_cutoff=threshold)

        if best_match:
            matched_title, best_score = best_match[0], best_match[1]  # 提取匹配的 title 和分数
            # 查找对应的 entity_uri
            entity_uri = next((uri for uri, title in self.data_entities.items() if title == matched_title), None)
            entity_id = entity_uri.split('/')[-1:][0]
            if entity_uri:
                matching_results[entity_id] = matched_title

        return matching_results

    def entity_extractor(self, query)->list:
        '''extract entity and return a list(or dictionary) of the entity'''
        # results = self.ner_pipeline(query)
        # entities = {result['word']: result['entity_group'] for result in results}        
        # return entities
        results = self.ner_pipeline(query)
        # print(results)
        entities = []
        current_entity = ""
        current_label = None
        current_start = None

        for i, result in enumerate(results):
            word = result['word'].replace("##", "")  # Remove '##' from subword tokens
            if word.startswith("##"):
                word = word[2:]  # Remove '##' prefix if still present after replacement

            if i > 0 and result['entity_group'] == results[i - 1]['entity_group'] and result['start'] == current_start + 1:
                # If the current entity group is the same as the previous one and they are consecutive, merge them
                current_entity += word
                current_start = result['end']
            else:
                # Append the previous entity to the list
                if current_entity:
                    entities.append({"word": current_entity.strip(), "entity": current_label})
                # Start a new entity group
                current_entity = word
                current_label = result['entity_group']
                current_start = result['end']

        # Append the last entity
        if current_entity:
            entities.append({"word": current_entity.strip(), "entity": current_label})

        # Convert list of entities to dictionary format for return
        merged_entities = {}
        for entity in entities:
            if entity['entity'] in merged_entities:
                merged_entities[entity['entity']] += " " + entity['word']
            else:
                merged_entities[entity['entity']] = entity['word']

        # 匹配现有的entity
        if merged_entities:
            results = []

            for entity_value in merged_entities.values():
                matching_results = self._entity2id(str(entity_value))
                if matching_results:
                    results.append(matching_results)

        return results

    def relation_extractor(self, query) -> dict:
        '''Extract the relation/predict and return a dictionary with relation_id as keys'''

        with open('data.json', 'r') as json_file:
            self.loaded_relation_data = json.load(json_file)

        # 创建一个字典来存储匹配结果
        extracted_relations = {}

        # 检查 query 是否是字符串，如果是，则处理为单个句子
        if isinstance(query, str):
            query = [query]  # 将单个句子变为列表以保持一致的处理逻辑

        # 遍历句子列表，逐句进行解析和匹配
        for sentence in query:
            print(f"\nProcessing sentence: '{sentence}'")

            # 遍历每个关系标签
            for relation_id, relation_label in self.loaded_relation_data.items():
                # 检查关系标签是否在句子中
                if relation_label.lower() in sentence.lower():
                    # 如果匹配到，则将 relation_id 作为键，relation_label 作为值存入字典
                    extracted_relations[relation_id] = relation_label

        # 返回匹配到的关系字典 (键为 relation_id，值为 relation_label)
        return extracted_relations

        # relations = {}
        # doc = self.nlp(query)
        # # for ent in doc.ents
        # #     print(f'entity text:{ent.text}, label: {ent.label_}')
        # for token in doc:
        #     # print(token.dep_, token.pos_)
        #     if token.dep_ in ("ROOT", "acl", "advcl", "relcl") and token.pos_ == "VERB":
        #         subject = [w for w in token.children if w.dep_ in ("nsubj", "nsubjpass")]
        #         obj = [w for w in token.children if w.dep_ in ("dobj", "attr", "prep", "pobj")]
        #         if subject and obj:
        #             relations["relation"]= token.lemma_
        #     if token.dep_ in ("attr", "nsubj") and token.pos_ == "NOUN":
        #         obj = [w for w in token.children if w.dep_ in ("prep", "pobj")]
        #         if obj:
        #             relations["relation"]= token.lemma_
        # return relations

