from transformers import AutoTokenizer
from transformers import pipeline
import spacy

# step1: extract entity and relation
class Query_Processer:
    def __init__(self):
        self.nlp = spacy.load("en_core_web_sm")
        self.tokenizer = AutoTokenizer.from_pretrained("dbmdz/bert-large-cased-finetuned-conll03-english")
        self.ner_pipeline = pipeline("ner", model="dbmdz/bert-large-cased-finetuned-conll03-english", 
                        tokenizer=self.tokenizer,
                        aggregation_strategy = "simple")

    def entity_extractor(self, query)->dict:
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
        
        return merged_entities
    
    def relation_extractor(self, query)->dict:
        '''extract the relation/predict and return a list(or dictionary)'''
        # Use SpaCy to extract relationships from the query
        relations = {}
        doc = self.nlp(query)
        # for ent in doc.ents
        #     print(f'entity text:{ent.text}, label: {ent.label_}')
        for token in doc:
            # print(token.dep_, token.pos_)
            if token.dep_ in ("ROOT", "acl", "advcl", "relcl") and token.pos_ == "VERB":
                subject = [w for w in token.children if w.dep_ in ("nsubj", "nsubjpass")]
                obj = [w for w in token.children if w.dep_ in ("dobj", "attr", "prep", "pobj")]
                if subject and obj:
                    relations["relation"]= token.lemma_
            if token.dep_ in ("attr", "nsubj") and token.pos_ == "NOUN":
                obj = [w for w in token.children if w.dep_ in ("prep", "pobj")]
                if obj:
                    relations["relation"]= token.lemma_
        return relations




# step2: mapping the entity and relation using dictionary
# load the dictionaries:
# load the dictionaries
# with open('entity_ids.del', 'r') as ifile:
#     ent2id = {rdflib.term.URIRef(ent): int(idx) for idx, ent in csv.reader(ifile, delimiter='\t')}
#     id2ent = {v: k for k, v in ent2id.items()}
# with open('relation_ids.del', 'r') as ifile:
#     rel2id = {rdflib.term.URIRef(rel): int(idx) for idx, rel in csv.reader(ifile, delimiter='\t')}
#     id2rel = {v: k for k, v in rel2id.items()}




# step3: construct SPARQL query
