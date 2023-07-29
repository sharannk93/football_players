import pandas as pd

def load_players_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'players.csv')
    players_df = pd.read_csv('players.csv')
    # Perform any additional data processing if needed
    return players_df
