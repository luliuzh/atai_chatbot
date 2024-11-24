import numpy as np
import pandas as pd
import pickle
from sklearn.metrics import pairwise_distances

class Recommender:
    """
    A class to recommend movies based on shared attributes and similarity scores.
    """

    def __init__(self):
        # Load embeddings and mapping files
        self.entity_emb = np.load('data/entity_embeds.npy')
        with open('data/ent2id.pkl', 'rb') as f:
            self.ent2id = pickle.load(f)
        with open('data/id2ent.pkl', 'rb') as f:
            self.id2ent = pickle.load(f)
        with open('data/lbl2ent.pkl', 'rb') as f:
            self.lbl2ent = pickle.load(f)
        with open('data/ent2lbl.pkl', 'rb') as f:
            self.ent2lbl = pickle.load(f)

    def labels_to_indices(self, labels: set) -> list:
        """
        Convert a set of labels to corresponding entity indices.
        :param labels: A set of labels
        :return: A list of indices
        """
        input_indices = []
        for label in labels:
            entity_uri = self.lbl2ent.get(label)  # Map label to entity URI
            if entity_uri and entity_uri in self.ent2id:
                input_indices.append(self.ent2id[entity_uri])
        return input_indices

    def recommend_movies(self, labels: set) -> list:
        """
        Recommend the top three similar movies based on input labels.
        :param labels: A set or list of input labels
        :return: A list of top three recommended movie labels
        """
        # Convert labels to indices
        input_indices = self.labels_to_indices(labels)

        if not input_indices:
            raise ValueError("Input labels could not be mapped to any valid entities.")

        # Compute recommendations
        distances = []
        for ent_id in input_indices:
            dist = pairwise_distances(self.entity_emb[ent_id].reshape(1, -1), self.entity_emb).reshape(-1)
            distances.append(dist)

        # Average distances
        combined_dist = sum(distances) / len(distances)

        # Sort and exclude input entities
        most_likely = [
            idx for idx in combined_dist.argsort()
            if self.id2ent[idx] not in {self.id2ent[ent_id] for ent_id in input_indices}  # Exclude input entities
        ]

        # Get top three recommended movie labels
        similar_movies = [
            self.ent2lbl.get(self.id2ent[idx], "Unknown")
            for idx in most_likely[:3]
        ]
        return similar_movies




# Initialize the Recommender class
recommender = Recommender()

# Input label set
labels = {"The Lion King", "Beauty and the Beast", "Pocahontas"}

# Get recommended movies
try:
    similar_movies = recommender.recommend_movies(labels)
    print("Recommended Movies:")
    print(similar_movies)
except ValueError as e:
    print(f"Error: {e}")
