import spacy

class Recommender:
    '''
    input query
    return shared_attributes && similar movies list
    '''
    def __init__(self) -> None:     
        self.entities_attributes = []
        self.shared_attributes = []
        self.similar_movies = []
        self.entities = []

    # step 2: get movie attributes using sparql
    def _entities_attributes(self, entities)->list:
        '''
        input self.entities list[]
        return self.shared_attributes list[]
        '''
        pass

    # step 3: get shared/similar attributes
    def get_shared_attributes(self)->list:
        '''
        input self.attributes list[]
        return self.shared_attributes list[]
        '''
        pass

    # step 4: recommand movies using similarity 
    def recommend_movies(self)->list:
        '''
        input self.shared_attributes list[]
        return self.similar_movies list[]
        '''
        pass

# usecase
recommender = Recommender()
shared_attributes = recommender.get_shared_attributes()
similar_movies = recommender.recommend()
