import re

class IntentRecognizer:
    def __init__(self):
        self.sparql_keywords = ["SELECT", "WHERE", "PREFIX", "FILTER"]
        self.recommend_keywords = ["recommend", "suggest", "recommendation", "recommendations"]
        self.factural_or_embedding_keywords = ["who", "when", "what", "director", "direct", "directed","genre"]
        self.multimedia_keywords = ["looks like" , "picture" ,"look like" , "photo"]

    def recognize_intent(self, query: str) -> str:

        if any(keyword in query.strip().upper() for keyword in self.sparql_keywords):
            return "SPARSQL"

        elif any(keyword in query.strip().lower() for keyword in self.multimedia_keywords):
            return "Multimedia"

        elif any(keyword in query.strip().lower() for keyword in self.recommend_keywords):
            return "RECOMMEND"
        
        elif any(keyword in query.strip().lower() for keyword in self.factural_or_embedding_keywords):
            return "FACTUAL_OR_EMBEDDING"
        
        else:
            return "RANDOM"

