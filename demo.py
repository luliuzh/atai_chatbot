from speakeasypy import Speakeasy, Chatroom
from typing import List
import time
from rdflib import Graph
import re

DEFAULT_HOST_URL = 'https://speakeasy.ifi.uzh.ch'
listen_freq = 2
nt_file_path = '../atai_chatbot/data/14_graph.nt'


class Agent:
    def __init__(self, username, password):
        self.username = username
        # Initialize the Speakeasy Python framework and login.
        self.speakeasy = Speakeasy(host=DEFAULT_HOST_URL, username=username, password=password)
        self.speakeasy.login()  # This framework will help you log out automatically when the program terminates.
        self.graph = Graph()
        self.graph.parse(nt_file_path, format='turtle')

    # excute the query
    def __query_sparql(self, query:str) -> str:
        results = self.graph.query(query)
        if len(results) == 0:
            return ['No results found']
        else:
            return[str(row) for row, in results]
  
    def _is_sparql(self, query:str) -> bool:
        return re.search(r'(\bSELECT\b|\bPREFIX\b)', query, re.IGNORECASE)
    
    def _parse_query(self, query:str):
        instruction_part = ""
        sparql_part = ""
        sparql_match = re.search(r'(\bSELECT\b|\bPREFIX\b)', query, re.IGNORECASE)

        instruction_part = query[:sparql_match.start()].strip()
        sparql_part = query[sparql_match.start():].replace("'''", '').strip()

        return instruction_part, sparql_part

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
                    else:
                        room.post_messages(f"Received your message: '{message.message}' ")

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
