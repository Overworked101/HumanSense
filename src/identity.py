class IdentityModel:
    def __init__(self):
        self.identity_profiles = {
            "ARTISTIC": {
                "artistic_bias": 0.9,
                "mainstream_bias": 0.2,
                "novelty_seeking": 0.7
            },
            "BALANCED": {
                "artistic_bias": 0.5,
                "mainstream_bias": 0.5,
                "novelty_seeking": 0.5
            },
            "CASUAL": {
                "artistic_bias": 0.2,
                "mainstream_bias": 0.8,
                "novelty_seeking": 0.3
            },
            "EXPLORER": {
                "artistic_bias": 0.6,
                "mainstream_bias": 0.3,
                "novelty_seeking": 0.9
            }
        }

    def get_identity_vector(self, identity):
        identity = identity.upper()
        if identity not in self.identity_profiles:
            raise ValueError("Invalid identity selected")
        return self.identity_profiles[identity]
