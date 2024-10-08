import sys
from rdflib import Graph
from speakeasypy import Speakeasy, Chatroom
from typing import List
import time

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
nt_file_path = r'D:\dev\python\python-learn\ATAI\speakeasy-python-client-library\14_graph.nt'  # path to 14_graph.nt
listen_freq = 2


class Agent:
    def __init__(self, username, password):
        self.username = username
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()

    def __query_sparql(self, query: str) -> list:
        """ 执行 SPARQL 查询并返回结果 """
        graph = Graph()
        graph.parse(nt_file_path, format='turtle')
        results = graph.query(query)
        if len(results) == 0:
            return ["No results found."]
        else:
            return [list(row) for row in results]  # 返回每行结果的列表

    def listen(self):
        while True:
            rooms: List[Chatroom] = self.speakeasy.get_rooms(active=True)
            for room in rooms:
                if not room.initiated:
                    room.post_messages(f'Hello! This is a welcome message from {room.my_alias}.')
                    room.initiated = True

                for message in room.get_messages(only_partner=True, only_new=True):
                    print(f"\t- Chatroom {room.room_id} - new message #{message.ordinal}: '{message.message}' - {self.get_time()}")

                    # Assume the message contains a SPARQL query
                    query_result = self.__query_sparql(message.message)
                    print(query_result)
                    room.post_messages(query_result)
                    # Format the query result into a string to send back
                    if query_result:
                        result_message = "Query Result:\n" + "\n".join([" | ".join(row) for row in query_result])
                    else:
                        result_message = "No results found for your query."

                    room.post_messages(result_message)
                    room.mark_as_processed(message)

                for reaction in room.get_reactions(only_new=True):
                    print(f"\t- Chatroom {room.room_id} - new reaction #{reaction.message_ordinal}: '{reaction.type}' - {self.get_time()}")
                    room.post_messages(f"Received your reaction: '{reaction.type}' ")
                    room.mark_as_processed(reaction)

            time.sleep(listen_freq)

    @staticmethod
    def get_time():
        return time.strftime("%H:%M:%S, %d-%m-%Y", time.localtime())


if __name__ == '__main__':
    demo_bot = Agent("ancient-flame", "A3fcD1X4")
    demo_bot.listen()
