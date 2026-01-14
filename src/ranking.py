import numpy as np

class RankingEngine:
    def purpose_alignment(self, movie_attr, purpose_vector):
        diffs = []
        for key in ["emotional_intensity", "pace"]:
            diffs.append(abs(movie_attr[key] - purpose_vector[key]))
        return 1 - np.mean(diffs)

    def identity_alignment(self, movie_attr, identity_vector):
        familiarity = movie_attr["familiarity"]
        return (
            identity_vector["artistic_bias"] * (1 - familiarity)
            + identity_vector["mainstream_bias"] * familiarity
        )

    def final_score(
        self,
        semantic_similarity,
        movie_attr,
        purpose_vector,
        identity_vector,
        movie_friction,
        user_tolerance
    ):
        purpose_score = self.purpose_alignment(movie_attr, purpose_vector)
        identity_score = self.identity_alignment(movie_attr, identity_vector)
        friction_penalty = max(0, movie_friction - user_tolerance)

        score = (
            0.45 * semantic_similarity
            + 0.20 * purpose_score
            + 0.15 * identity_score
            - 0.20 * friction_penalty
        )

        return score
