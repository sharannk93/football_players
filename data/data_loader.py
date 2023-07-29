import pandas as pd

def load_players_data():
    players_df = pd.read_csv('players.csv')
    # Perform any additional data processing if needed
    return players_df
