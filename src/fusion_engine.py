import numpy as np
import pandas as pd

from src.embeddings import EmbeddingGenerator
from src.purpose import PurposeModel
from src.movie_attributes import MovieAttributeExtractor
from src.scoring import HumanSenseScorer

print("🔥 FusionEngine LOADED FROM:", __file__)

class FusionEngine:
    def __init__(self):
        self.embedder = EmbeddingGenerator()
        self.purpose_model = PurposeModel()
        self.attribute_extractor = MovieAttributeExtractor()
        self.scorer = HumanSenseScorer()

    def _compute_purpose_weight(self, purpose_vector, movie_attrs):
        """
        Compare purpose vector with movie attributes
        """
        diff = (
            abs(purpose_vector["emotional_intensity"] - movie_attrs["emotional_intensity"]) +
            abs(purpose_vector["pace"] - movie_attrs["pace"])
        )

        # Lower difference → higher weight
        return max(0.6, 1.2 - diff)

    def _compute_identity_bias(self, identity, movie_attrs):
        """
        Bias based on self-identity vs familiarity
        """
        familiarity = movie_attrs["familiarity"]

        if identity == "artistic":
            return 1.2 if familiarity < 0.5 else 0.8
        elif identity == "casual":
            return 1.2 if familiarity >= 0.5 else 0.9
        else:
            return 1.0

    def _compute_cognitive_penalty(self, tolerance, movie_attrs):
        """
        Penalize overload
        """
        overload = (
            movie_attrs["emotional_intensity"] +
            movie_attrs["pace"]
        ) / 2

        if overload > tolerance:
            return min(0.5, overload - tolerance)
        return 0.0

    def _apply_novelty_comfort(
        self,
        base_score,
        familiarity,
        novelty_preference
    ):
        """
        Adjust score based on novelty vs comfort preference
        novelty_preference ∈ [0, 1]
        """

        novelty_preference = max(0.0, min(1.0, novelty_preference))

        novelty_score = 1.0 - familiarity

        adjustment = (
            (1 - novelty_preference) * familiarity +
            novelty_preference * novelty_score
        )

        return base_score * adjustment

    def recommend(self, movies_df, user_profile, top_k=10):

        # Step 1: Embeddings
        movie_embeddings = self.embedder.build_movie_embeddings(movies_df)
        user_vector = self.embedder.build_user_embedding(
            user_profile["purpose_description"]
        )

        similarities = (
            movie_embeddings @ user_vector
        ) / (
            np.linalg.norm(movie_embeddings, axis=1) * np.linalg.norm(user_vector)
        )

        print("Similarities shape:", similarities.shape)

        # Step 2: Purpose Vector
        purpose_vector = self.purpose_model.get_purpose_vector(
            user_profile["purpose"]
        )

        n_movies = len(movies_df)
        scores = np.zeros(n_movies)

        for i, (_, row) in enumerate(movies_df.iterrows()):
            movie_attrs = self.attribute_extractor.extract_attributes(row)

            purpose_weight = self._compute_purpose_weight(
                purpose_vector, movie_attrs
            )
            identity_bias = self._compute_identity_bias(
                user_profile["identity"], movie_attrs
            )

            cognitive_penalty = self._compute_cognitive_penalty(
                user_profile["cognitive_tolerance"], movie_attrs
            )

            scores[i] = (
            similarities[i]
            * purpose_weight
            * identity_bias
            * (1 - cognitive_penalty)
        )
        
        movies_df = movies_df.copy()
        movies_df["humanSense_score"] = scores


        movies_df = movies_df.drop_duplicates(subset="id")


        return movies_df.sort_values(
            by="humanSense_score",
            ascending=False
        ).head(top_k)
