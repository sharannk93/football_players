import pandas as pd
import os

def load_players_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    file_path = os.path.join(current_dir, 'players.csv')
    try:
        players_df = pd.read_csv(file_path)
        return players_df
    except Exception as e:
        # Print the error message to a local log file
        with open('data_loader_error_log.txt', 'a') as f:
            f.write(str(e) + '\n')
        # Return an empty DataFrame or None to indicate an error
        return pd.DataFrame()  # or return None if you prefer
