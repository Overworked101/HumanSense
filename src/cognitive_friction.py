class CognitiveFrictionModel:
    def compute_movie_friction(self, movie_attributes):
        duration = movie_attributes["duration"]
        emotional_intensity = movie_attributes["emotional_intensity"]
        pace = movie_attributes["pace"]
        familiarity = movie_attributes["familiarity"]

        friction = (
            0.35 * duration +
            0.35 * emotional_intensity +
            0.20 * (1 - pace) +
            0.10 * (1 - familiarity)
        )

        return min(friction, 1.0)

    def compute_user_tolerance(self, purpose_vector, identity_vector):
        # Cognitive tolerance depends on purpose + identity
        tolerance = (
            0.6 * purpose_vector["cognitive_tolerance"] +
            0.4 * identity_vector["novelty_seeking"]
        )

        return min(tolerance, 1.0)
