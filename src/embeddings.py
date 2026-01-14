from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    """
    Generates semantic embeddings for movies using SBERT
    """

    def __init__(self):
        # Lightweight, fast, very popular model
        self.model = SentenceTransformer("all-MiniLM-L6-v2")

    def build_movie_embeddings(self, df):
        """
        Combines overview + genres and encodes them safely
        """

        texts = (
        df["overview"].fillna("").astype(str)
        + " "
        + df["joined_genre"].fillna("").astype(str)
        ).tolist()

        embeddings = self.model.encode(
            texts,
            show_progress_bar=True
        )
        return np.array(embeddings)
    
    def build_user_embedding(self, text):
        """
        Generates embedding for user intent / purpose description
        """
        text = str(text)
        embedding = self.model.encode([text])
        return embedding[0]

from sklearn.metrics.pairwise import cosine_similarity
import numpy as np

class MovieSimilarityEngine:
    """
    Retrieves similar movies using cosine similarity
    """

    def __init__(self, embeddings):
        self.embeddings = embeddings

    def recommend(self, movie_index, top_k=10):
        """
        Returns indices and similarity scores of top_k similar movies
        """
        query_vector = self.embeddings[movie_index].reshape(1, -1)

        similarities = cosine_similarity(
            query_vector,
            self.embeddings
        )[0]

        # Sort by similarity score
        similar_indices = np.argsort(similarities)[::-1]

        # Remove the movie itself
        similar_indices = similar_indices[similar_indices != movie_index]

        return similar_indices[:top_k], similarities[similar_indices[:top_k]]
