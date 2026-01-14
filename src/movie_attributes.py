import pandas as pd

class MovieAttributeExtractor:
    def __init__(self):
        self.high_emotion_genres = {"Drama", "Romance"}
        self.low_emotion_genres = {"Animation", "Family"}
        self.fast_pace_genres = {"Action", "Thriller", "Crime", "Adventure"}

    def extract_attributes(self, row):
        attributes = {}

        # Duration
        runtime = row["runtime"] if not pd.isna(row["runtime"]) else 90
        attributes["duration"] = min(runtime / 180, 1.0)

        # Emotional intensity
        genres = set(row["genres"])

        if genres & self.high_emotion_genres:
            attributes["emotional_intensity"] = 0.8
        elif genres & self.low_emotion_genres:
            attributes["emotional_intensity"] = 0.3
        else:
            attributes["emotional_intensity"] = 0.5

        # Pace
        if genres & self.fast_pace_genres:
            attributes["pace"] = 0.8
        elif runtime > 120:
            attributes["pace"] = 0.4
        else:
            attributes["pace"] = 0.6

        # Familiarity (mainstream score)
        popularity = row["popularity"]
        attributes["familiarity"] = min(popularity / 50, 1.0)

        return attributes
