import pandas as pd
import os

def load_players_data():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    st.write("Current Directory:", current_dir)
    
    file_path = os.path.join(current_dir, 'players.csv')
    st.write("File Path:", file_path)
    
    players_df = pd.read_csv(file_path)
    # Perform any additional data processing if needed
    return players_df
