import pandas as pd
import ast
from sklearn.preprocessing import MinMaxScaler

class Preprocessor:
    """
    Handles all preprocessing steps for the HumanSense system
    """

    def __init__(self):
        self.scaler = MinMaxScaler()

    def load_data(self, path):
        """
        Loads dataset from CSV
        """
        return pd.read_csv(path)

    def parse_genres(self, x):
        """
        Converts stringified JSON genre field into list of genre names
        """
        try:
            genres = ast.literal_eval(x)
            return [g['name'] for g in genres]
        except:
            return []

    def clean(self, df):
        """
        Performs cleaning operations
        """
        df['overview'] = df['overview'].fillna("")
        df['runtime'] = df['runtime'].fillna(df['runtime'].median())
        df['genres'] = df['genres'].apply(self.parse_genres)
        df['joined_genre'] = df['genres'].apply(lambda x: " ".join(x))
        return df

    def scale_features(self, df, columns):
        """
        Normalizes numerical columns between 0 and 1
        """
        df[columns] = self.scaler.fit_transform(df[columns])
        return df
