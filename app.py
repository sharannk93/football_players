import streamlit as st
import pandas as pd
import plotly.express as px
from sklearn.metrics.pairwise import cosine_similarity

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
action = st.radio('What do you want to do', ('Compare selected players of your choice', 'Scout players based on your criteria', 'Find similar players'))

# Button to explain scoring
explain_scoring_button = st.button("Explain scoring")

# Placeholder for the explanation text
explanation_placeholder = st.empty()

# Explanation text to be displayed
explanation_text = """
Sure! Let's explain the scoring calculation for each KPI in simple words:

Shooting: This score is calculated by adding two factors - the number of goals per 90 minutes played and the shot-to-goal conversion rate. So, it considers how often a player scores and how efficient they are in converting their shots into goals.

Vision: The score for Vision is simply the number of key passes (important passes that lead to goal-scoring opportunities) per 90 minutes played. It measures the player's ability to create scoring chances for their teammates.

Crossing: The Crossing score is based on the number of accurate crosses (well-placed passes into the opponent's penalty area) per 90 minutes played. It shows the player's proficiency in delivering effective crosses to set up goal-scoring opportunities.

Dribbling: This score represents the number of successful dribbles per 90 minutes played. It indicates how skilled the player is at maneuvering the ball past opponents by dribbling.

Possession: The Possession score is determined by the ratio of completed passes to total passes per 90 minutes played. It reflects the player's ability to maintain possession of the ball through accurate passing.

Interceptions: This score is based on the number of interceptions made per 90 minutes played. It measures the player's capability to read the game and disrupt the opponent's attacks by intercepting their passes.

Tackling: The Tackling score is calculated using the number of successful tackles per 90 minutes played. It shows how proficient the player is in winning the ball back from the opponent through tackling.

Aerials won: This score is obtained by dividing the total number of aerial duels won by the player over all matches by the total minutes played. It represents the player's ability to win aerial challenges, such as headers.

Each of these scores evaluates a specific aspect of a player's performance in a soccer match and helps in understanding their strengths and contributions to the team.

After calculating each player's score for each KPI, their scores are then compared to all the other players in the dataset. The scores are scaled that they range from 0 to 100, with 100 representing the best possible score and 0 indicating the worst possible score for that particular KPI.

This scaling process allows for a fair comparison among players and makes it easier to understand their relative strengths and weaknesses in each aspect of the game. So, a player with a score of 100 in a specific KPI is considered the best performer in that category, while a player with a score of 0 has the most room for improvement in that particular area. All other players' scores fall somewhere in between based on their performance compared to others.

By scaling the scores from 0 to 100, it becomes much simpler to identify and rank players based on their overall contributions and abilities in various aspects of soccer.
"""

# Display explanation text when the button is clicked
if explain_scoring_button:
    explanation_placeholder.markdown(explanation_text)

# Rest of your code for Option 1 and Option 2...



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


# Option 3: Find similar players
elif action == 'Find similar players':
    st.write("Select your player")
    selected_player = st.selectbox('Select player', players_df['full_name'].unique())

    st.write("Select age")
    selected_age = st.slider('Select age', min_value=int(players_df['age'].min()), max_value=int(players_df['age'].max()), value=(int(players_df['age'].min()), int(players_df['age'].max())))

    st.write("Select league")
    selected_leagues = st.multiselect('Select league', players_df['league'].unique(), default=players_df['league'].unique())

    # Filter data based on selected player, age, and league
    filtered_players_df = players_df[
        (players_df['full_name'] != selected_player) &
        (players_df['age'] >= selected_age[0]) &
        (players_df['age'] <= selected_age[1]) &
        (players_df['league'].isin(selected_leagues))
    ]

    # Select the player data
    selected_player_data = players_df[players_df['full_name'] == selected_player][['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won']]

    # Calculate cosine similarity between the selected player and other players
    similarity_scores = cosine_similarity(selected_player_data, filtered_players_df[['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won']])

    # Add similarity scores to the filtered dataframe
    filtered_players_df['Similarity score'] = similarity_scores[0]

    # Sort the dataframe by similarity score and select the top 5 similar players
    top_5_similar_players = filtered_players_df.sort_values(by='Similarity score', ascending=False).head(5)

    # Display the table with the top 5 similar players
    st.write("Top 5 most similar players:")
    st.dataframe(top_5_similar_players[['full_name', 'age', 'league', 'Similarity score']])

    # Radar chart for the selected player and the top 5 similar players
    radar_data = pd.concat([selected_player_data, top_5_similar_players[['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won']]])
    radar_data['Player'] = [selected_player] + list(top_5_similar_players['full_name'])
    radar_data_melted = pd.melt(radar_data, id_vars=['Player'], value_vars=['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won'], var_name='attribute', value_name='score')

    fig_radar = px.line_polar(radar_data_melted, r='score', theta='attribute', line_close=True, color='Player')

    # Update the legend and attribute label font size
    fig_radar.update_layout(legend=dict(font=dict(size=14)), polar=dict(radialaxis=dict(tickfont=dict(size=14))))

    # Function to get the color of the player from the plotly figure
    def get_player_color(player_name):
        for trace in fig_radar.data:
            if trace.name == player_name:
                return trace.line.color[0]
        return None

    # Highlight player with the highest value in each attribute
    for attribute in ['Shooting', 'Vision', 'Possession', 'Crossing', 'Dribbling', 'Interceptions', 'Tackling', 'Aerials won']:
        max_player_name = radar_data.loc[radar_data[attribute].idxmax(), 'Player']
        max_player_score = radar_data.loc[radar_data[attribute].idxmax(), attribute]
        player_color = get_player_color(max_player_name)
        if player_color:
            st.markdown(f"<span style='color:{player_color}'>{max_player_name}</span> has the best <b>{attribute}</b> score of <b>{max_player_score}</b> from the selected players.", unsafe_allow_html=True)

    st.plotly_chart(fig_radar)