import numpy as np

class HumanSenseScorer:
    def __init__(self):
        pass

    def compute_score(
        self,
        semantic_similarity,
        purpose_weight,
        identity_bias,
        cognitive_penalty
    ):
        """
        Final HumanSense scoring function
        """
        score = (
            semantic_similarity
            * purpose_weight
            * identity_bias
            * (1 - cognitive_penalty)
        )
        return score
