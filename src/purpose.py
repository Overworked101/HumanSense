class PurposeModel:
    def __init__(self):
        self.purpose_profiles = {
            "RELAX": {
                "emotional_intensity": 0.2,
                "pace": 0.3,
                "cognitive_tolerance": 0.2
            },
            "UPLIFT": {
                "emotional_intensity": 0.7,
                "pace": 0.6,
                "cognitive_tolerance": 0.5
            },
            "DISTRACT": {
                "emotional_intensity": 0.5,
                "pace": 0.8,
                "cognitive_tolerance": 0.3
            },
            "EXPLORE": {
                "emotional_intensity": 0.8,
                "pace": 0.5,
                "cognitive_tolerance": 0.9
            }
        }

    def get_purpose_vector(self, purpose):
        purpose = purpose.upper()
        if purpose not in self.purpose_profiles:
            raise ValueError("Invalid purpose selected")
        return self.purpose_profiles[purpose]
