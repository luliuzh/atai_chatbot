class Recommender:
    '''
    input query
    return shared_attributes && similar movies list
    '''
    def __init__(self, query) -> None:
        self.query = query
        self.entities = []
        self.entities_attributes = []
        self.shared_attributes = []
        self.similar_movies = []

    # step 1: extract movie entities using Query_processer
    def _entities_extractor(self)->list:
        '''
        input query
        return self.entities list[]
        '''
        pass

    # step 2: get movie attributes using sparql
    def _entities_attributes(self)->list:
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
    def recommend(self)->list:
        '''
        input self.shared_attributes list[]
        return self.similar_movies list[]
        '''
        pass

# usecase
query = ""
recommender = Recommender(query)
shared_attributes = recommender.get_shared_attributes()
similar_movies = recommender.recommend()
