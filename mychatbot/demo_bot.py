
import sys
from pydantic import Extra
import rdflib
from rdflib import Graph
from speakeasypy import Speakeasy, Chatroom
from typing import List
import time
import re
import unicodedata
from factual_q import Query_Processer
from  Embedding_q import get_closest_entity
from Intent_recognizer import IntentRecognizer
from new_recommendor import Recommender
from MultiMedia import multimedia_handler
import pickle


DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'

nt_file_path = r'data\14_graph.nt'


listen_freq = 3
pickle_file = "data/14_graph.pickle"
# 定义命名空间
WD = rdflib.Namespace('http://www.wikidata.org/entity/')
WDT = rdflib.Namespace('http://www.wikidata.org/prop/direct/')
DDIS = rdflib.Namespace('http://ddis.ch/atai/')
RDFS = rdflib.namespace.RDFS
SCHEMA = rdflib.Namespace('http://schema.org/')

with open("data/14_graph.pickle", "rb") as f:
            graph = pickle.load(f)


class Agent:
    def __init__(self, username, password):
        self.username = username
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()
        # self.graph = Graph()
        # self.graph.parse(nt_file_path, format='turtle')
        # 直接加载 pickle 文件
        self.graph = graph

        self.my_intent_recognizer = IntentRecognizer()
        self.my_query_processer = Query_Processer(self.graph)
        self.my_recommender = Recommender()
    
    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            try:
                rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            except Exception as e:
                print(f"Error fetching rooms: {e}")
                continue  # Skip this iteration on failure

            for room in rooms:
                try:
                    if not room.initiated:
                        # send a welcome message if room is not initiated
                        room.post_messages(f'Hello! This is a welcome message from {room.my_alias}.')
                        room.initiated = True
                    # Retrieve messages from this chat room.
                    # If only_partner=True, it filters out messages sent by the current bot.
                    # If only_new=True, it filters out messages that have already been marked as processed.
                    for message in room.get_messages(only_partner=True, only_new=True):
                        print(
                            f"\t- Chatroom {room.room_id} "
                            f"- new message #{message.ordinal}: '{message.message}' "
                            f"- {self.get_time()}")

                        # Implement your agent here #
                        query = message.message

                        # distinguish intent
                        intent = self.my_intent_recognizer.recognize_intent(query)

                        if intent == "SPARSQL":
                            # parse the query
                            _, sparql_part = self._parse_query(query)
                            # excute the query
                            print(f'executing the query...')
                            query_result = self._query_sparql(sparql_part)
                            if query_result == "NO_RESULTS":
                                response_message = "sorry no matching answer"
                            elif query_result == "ERROR":
                                response_message = "something went wrong."
                            else:
                                response_message = f"here is the searching result: {query_result}"

                        elif intent == "FACTUAL_OR_EMBEDDING":
                            print(f'processing the factual or embedding query...')
                            entity = self.my_query_processer.entity_extractor(query)
                            relation = self.my_query_processer.relation_extractor(query, entity)
                            for entity_item, relation_item in zip(entity, relation.values()):
                                entity_value = list(entity_item.values())[0]
                                relation_value = relation_item
                                    # 调用 get_closest_entity 函数并存储结果
                                response_message = get_closest_entity(self.graph, entity_label=entity_value,
                                                                relation_label=relation_value)
                                if response_message == None:
                                    response_message = "Sorry ,I dont find answer in my database"
                                else:
                                    response_message = ( f"Closest entity for {entity_value} with relation {relation_value}: {response_message}")  # 输出结果
                        
                        elif intent == 'RECOMMEND':
                            print(f'processing recommend query...')
                            entities = self.my_query_processer.entity_extractor_recommender(query)
                            movies = [list(item.values())[0] for item in entities]
                            # if movies = none , give a template answer
                            recommend_movies = self.my_recommender.recommend_movies(movies)
                            common_features = self.my_recommender._common_feature(movies)
                            # 如果列表有多个元素，进行格式化处理
                            if len(common_features) > 1:
                                feature_str = ', '.join(common_features[:-1]) + f' and {common_features[-1]}'
                            else:
                                feature_str = common_features[0] if common_features else "no feature"
                            if len(recommend_movies) > 1:
                                movies_str = ', '.join(recommend_movies[:-1]) + f' and {recommend_movies[-1]}'
                            else:
                                # 如果只有一个电影
                                movies_str = recommend_movies[0] if recommend_movies else "no movies"

                            response_message = f"The movies you mentioned share common features like {feature_str}. Based on these, I recommend similar movies such as {movies_str}."

                            print(response_message)
                            # shared_attributes = self.my_recommender.get_shared_attributes(entities)
                            # recommend_movies = self.my_recommender.recommend_movies(entities)
                            # response_message = f'Adequate recommendations will be {shared_attributes}, such as the movies {recommend_movies}'


                        elif intent == 'Multimedia':
                            # response_message ="image:2889/rm1919332864"
                            print(f'processing Multimedia...')
                            Extracted_entities = self.my_query_processer.entity_extractor_recommender(query)
                            entities = [list(item.values())[0] for item in Extracted_entities]
                            print(entities)
                            multimedia = multimedia_handler(self.graph)
                            response_message = multimedia.show_img(entities)
                         
                        
                        elif intent == 'RANDOM':
                            print(f'processing random query...')
                            response_message = f"Hello, do you have any questions?"
                        
                        room.post_messages(response_message)
                        room.mark_as_processed(message)  
                        print(f'response for the query:{response_message}')


                except Exception as e:
                    print(f"Error in processing room {room.room_id}: {e}")
                    continue  # Skip this room on error

                # Retrieve reactions from this chat room.
                # If only_new=True, it filters out reactions that have already been marked as processed.
                for reaction in room.get_reactions(only_new=True):
                    print(
                        f"\t- Chatroom {room.room_id} "
                        f"- new reaction #{reaction.message_ordinal}: '{reaction.type}' "
                        f"- {self.get_time()}")

                    # Implement your agent here #
                    room.post_messages(f"Received your reaction: '{reaction.type}' ")
                    room.mark_as_processed(reaction)

            time.sleep(listen_freq)

    @staticmethod
    def get_time():
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())
    
    def _parse_query(self, query:str):
        instruction_part = ""
        sparql_part = ""
        sparql_match = re.search(r'(\bSELECT\b|\bPREFIX\b)', query, re.IGNORECASE)

        instruction_part = query[:sparql_match.start()].strip()
        sparql_part = query[sparql_match.start():].replace("'''", '').strip()

        return instruction_part, sparql_part
    
    def _query_sparql(self, query: str) -> list:
        """ 执行 SPARQL 查询并返回结果 """
        try:
            results = self.graph.query(query)
            # 提取字符串结果
            extracted_results = [str(row[0]) for row in results]
            if not extracted_results:  # Check if extracted_results is empty
                return "NO_RESULTS"                 
            # Join the extracted results into a single string
            extracted_results = ", ".join(extracted_results)
            # remove non-ASCII characters
            extracted_results = unicodedata.normalize('NFKD', extracted_results)
            extracted_results = re.sub(r'[^\x00-\x7F]+', '', extracted_results) 
            return extracted_results.encode('utf-8').decode('utf-8') # Return as a formatted string    
        except Exception as e:
            return "ERROR"

if __name__ == '__main__':
    demo_bot = Agent("ancient-flame", "A3fcD1X4")
    demo_bot.listen()
