import sys
from rdflib import Graph
from speakeasypy import Speakeasy, Chatroom
from typing import List
import time
import re

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
# nt_file_path = r'D:\dev\python\python-learn\ATAI\speakeasy-python-client-library\14_graph.nt'  # path to 14_graph.nt
nt_file_path = '../atai_chatbot/data/14_graph.nt'
listen_freq = 3



class Agent:
    def __init__(self, username, password):
        self.username = username
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()
        self.graph = Graph()
        self.graph.parse(nt_file_path, format='turtle')

    # def __query_sparql(self, query: str) -> list:
    #     """ 执行 SPARQL 查询并返回结果 """
    #
    #     results = self.graph.query(query)
    #     print(results)
    #     result_list = list(results)  # 将结果转换为列表
    #     if not result_list:
    #         return ["No results found."]
    #     else:
    #         return [list(row) for row in result_list]  # 返回每行结果的列表
    def _is_sparql(self, query:str) -> bool:
        return re.search(r'(\bSELECT\b|\bPREFIX\b)', query, re.IGNORECASE)
    
    def _parse_query(self, query:str):
        instruction_part = ""
        sparql_part = ""
        sparql_match = re.search(r'(\bSELECT\b|\bPREFIX\b)', query, re.IGNORECASE)

        instruction_part = query[:sparql_match.start()].strip()
        sparql_part = query[sparql_match.start():].replace("'''", '').strip()

        return instruction_part, sparql_part
    
    def __query_sparql(self, query: str) -> list:
            """ 执行 SPARQL 查询并返回结果 """
            results = self.graph.query(query)

            # 提取字符串结果
            extracted_results = [str(row[0]) for row in results]

            if len(extracted_results) == 0:
                return ["No results found."]
            else:
                return extracted_results  # 返回结果列表

    def listen(self):
        while True:
            # only check active chatrooms (i.e., remaining_time > 0) if active=True.
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
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
                    print(message.message)
                    # query_result = self.__query_sparql(f"""{message.message}""")
                    # # Send a message to the corresponding chat room using the post_messages method of the room object.
                    # # room.post_messages(f"Received your message: '{message.message}' ")
                    # room.post_messages(str(query_result))
                    # # Mark the message as processed, so it will be filtered out when retrieving new messages.
                    # room.mark_as_processed(message)
                    # Implement your agent here #
                    query = message.message
                    # distinguish if the query is a sparql
                    if self._is_sparql(query):
                        # parse the query
                        _, sparql_part = self._parse_query(query)
                        # excute the query
                        query_result = self.__query_sparql(sparql_part)
                        print(f"log_info:{query_result}")
                        # generate the response
                        response_message = f"here is the searching result: '{query_result}'"
                        # post the result to user
                        room.post_messages(response_message)

                    # Mark the message as processed, so it will be filtered out when retrieving new messages.
                    room.mark_as_processed(message)

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

if __name__ == '__main__':
    demo_bot = Agent("ancient-flame", "A3fcD1X4")
    demo_bot.listen()
