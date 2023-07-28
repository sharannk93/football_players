import streamlit as st
import pandas as pd
import plotly.express as px

# Load the CSV file
players_df = pd.read_csv('players.csv')

# Set bigger font size for the whole app
st.markdown(
    """
    <style>
    body {
        font-size: 38px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Custom CSS to align the title to the left
st.markdown(
    """
    <style>
    .title {
        text-align: left;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Title of the page aligned to the left
st.title('Football Player Analysis')

# Question: What do you want to do?
action = st.radio('What do you want to do', ('Compare selected players of your choice', 'Scout players based on your criteria'))



# Option 1: Compare selected players
if action == 'Compare selected players of your choice':
    st.write("Select players to compare")
    selected_players = st.multiselect('Select players', players_df['full_name'].unique())

    if selected_players:
        # Filter the DataFrame for selected players
        selected_players_df = players_df[players_df['full_name'].isin(selected_players)]

        # Reshape the DataFrame to have attributes as values in a separate column
        selected_players_melted = pd.melt(selected_players_df, id_vars=['full_name'], value_vars=[
            'Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling',
            'Interceptions', 'Tackling', 'Aerials won'], var_name='attribute', value_name='score')

        # Radar chart
        fig = px.line_polar(selected_players_melted, r='score', theta='attribute', line_close=True, color='full_name')

        # Update the legend and attribute label font size
        fig.update_layout(legend=dict(font=dict(size=14)), polar=dict(radialaxis=dict(tickfont=dict(size=14))))

        # Function to get the color of the player from the plotly figure
        def get_player_color(player_name):
            for trace in fig.data:
                if trace.name == player_name:
                    return trace.line.color[0]
            return None

        # Highlight player with the highest value in each attribute
        for attribute in ['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won']:
            max_player_name = selected_players_df.loc[selected_players_df[attribute].idxmax(), 'full_name']
            max_player_score = selected_players_df.loc[selected_players_df[attribute].idxmax(), attribute]
            player_color = get_player_color(max_player_name)
            if player_color:
                st.markdown(f"<span style='color:{player_color}'>{max_player_name}</span> has the best <b>{attribute}</b> score of <b>{max_player_score}</b> from the players selected.", unsafe_allow_html=True)

        st.plotly_chart(fig)

# Option 2: Scout players based on criteria
elif action == 'Scout players based on your criteria':
    # Question 1: Which position do you want to scout?
    selected_positions = st.multiselect('Which position do you want to scout?', players_df['position'].unique(), default=players_df['position'].unique())

    # Question 2: Which league do you want to scout?
    selected_leagues = st.multiselect('Which league do you want to scout?', players_df['league'].unique(), default=players_df['league'].unique())

    # Question 3: Do you have any age preference?
    min_age, max_age = st.slider('Select age range', min_value=int(players_df['age'].min()), max_value=int(players_df['age'].max()), value=(int(players_df['age'].min()), int(players_df['age'].max())))

    # Question 4: Select shooting score range
    min_shooting, max_shooting = st.slider('Select shooting score range', min_value=float(players_df['Shooting'].min()), max_value=float(players_df['Shooting'].max()), value=(float(players_df['Shooting'].min()), float(players_df['Shooting'].max())))

    # Question 5: Select vision score range
    min_vision, max_vision = st.slider('Select vision score range', min_value=float(players_df['Vision'].min()), max_value=float(players_df['Vision'].max()), value=(float(players_df['Vision'].min()), float(players_df['Vision'].max())))

    # Question 6: Select crossing score range
    min_crossing, max_crossing = st.slider('Select crossing score range', min_value=float(players_df['Crossing'].min()), max_value=float(players_df['Crossing'].max()), value=(float(players_df['Crossing'].min()), float(players_df['Crossing'].max())))

    # Question 7: Select dribbling score range
    min_dribbling, max_dribbling = st.slider('Select dribbling score range', min_value=float(players_df['Dribbling'].min()), max_value=float(players_df['Dribbling'].max()), value=(float(players_df['Dribbling'].min()), float(players_df['Dribbling'].max())))

    # Question 8: Select possession score range
    min_possession, max_possession = st.slider('Select possession score range', min_value=float(players_df['Possession'].min()), max_value=float(players_df['Possession'].max()), value=(float(players_df['Possession'].min()), float(players_df['Possession'].max())))

    # Question 9: Select interceptions score range
    min_interceptions, max_interceptions = st.slider('Select interceptions score range', min_value=float(players_df['Interceptions'].min()), max_value=float(players_df['Interceptions'].max()), value=(float(players_df['Interceptions'].min()), float(players_df['Interceptions'].max())))

    # Question 10: Select tackling score range
    min_tackling, max_tackling = st.slider('Select tackling score range', min_value=float(players_df['Tackling'].min()), max_value=float(players_df['Tackling'].max()), value=(float(players_df['Tackling'].min()), float(players_df['Tackling'].max())))

    # Question 11: Select aerials won score range
    min_aerials_won, max_aerials_won = st.slider('Select aerials won score range', min_value=float(players_df['Aerials won'].min()), max_value=float(players_df['Aerials won'].max()), value=(float(players_df['Aerials won'].min()), float(players_df['Aerials won'].max())))

    # Filter data based on selected criteria
    filtered_df = players_df[
        (players_df['position'].isin(selected_positions)) &
        (players_df['league'].isin(selected_leagues)) &
        (players_df['age'] >= min_age) &
        (players_df['age'] <= max_age) &
        (players_df['Shooting'] >= min_shooting) &
        (players_df['Shooting'] <= max_shooting) &
        (players_df['Vision'] >= min_vision) &
        (players_df['Vision'] <= max_vision) &
        (players_df['Crossing'] >= min_crossing) &
        (players_df['Crossing'] <= max_crossing) &
        (players_df['Dribbling'] >= min_dribbling) &
        (players_df['Dribbling'] <= max_dribbling) &
        (players_df['Possession'] >= min_possession) &
        (players_df['Possession'] <= max_possession) &
        (players_df['Interceptions'] >= min_interceptions) &
        (players_df['Interceptions'] <= max_interceptions) &
        (players_df['Tackling'] >= min_tackling) &
        (players_df['Tackling'] <= max_tackling) &
        (players_df['Aerials won'] >= min_aerials_won) &
        (players_df['Aerials won'] <= max_aerials_won)
    ]

    # Display the filtered table with specific columns
    columns_to_display = [
        'full_name', 'age', 'league', 'position', 'Current Club',
        'Shooting', 'shot/goal conversion', 'Vision', 'Crossing', 'Dribbling',
        'Possession', 'Interceptions', 'Tackling', 'Aerials won', 'Defense'
    ]
    st.dataframe(filtered_df[columns_to_display], width=800, height=None)
