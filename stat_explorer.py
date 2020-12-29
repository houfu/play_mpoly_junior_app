from collections import Counter

import altair as alt
import pandas as pd
import streamlit as st


def stat_explorer(num_players):
    global data, board_spaces
    st.title('Mpoly Junior Game statistics explorer')
    st.write("""
    We play 5,000,000 games. Use the radio buttons at the sidebar to change the number of players in the game.
    """)
    with st.beta_expander('Notes'):
        st.write("""

        * The games are played under advanced rules -- if a player is bankrupt, the player can sell property 
        to the creditor. Games end when all players are truly bankrupt or the games last longer than 
        300 rounds (a draw).
        * Some algorithms are in place to mimic decisions made in an actual game. For example:
            * If a player has a choice to move to a space where there is liability for paying rent, and one that 
            does not, player chooses the free space.
            * If a player has to sell property to a bank or player, it chooses the least expensive property first.
            * If a player gets a choice to pick a property to buy, it picks the most expensive one that would make 
            a pair.

        """)

    @st.cache
    def load_data(no_of_players: int):
        data_to_be_loaded = pd.read_csv(f'games_{no_of_players}p_5m.csv.gz', compression='gzip')
        data_to_be_loaded.index.name = 'Game'
        return data_to_be_loaded

    with st.spinner('Loading data...'):
        data = load_data(num_players)
    st.header('Win Percentage')
    st.write("""
    What are the odds of 1 player winning? This shows how significant the 1st player's advantage is, and how 
    many games end in a draw (more than 300 rounds).
    
    (Incidentally, the youngest player is designated the first player in the junior game.)
    """)

    @st.cache
    def compile_win_percentages(players: int, data, games=5000000):
        winners = data['winner'].value_counts().to_dict()
        if num_players == 2:
            result = pd.DataFrame({'player': ['Player 1', 'Player 2', 'Draw'],
                                   'Win Count': [winners[0], winners[1], winners[-1]]})
        elif num_players == 3:
            result = pd.DataFrame({'player': ['Player 1', 'Player 2', 'Player 3', 'Draw'],
                                   'Win Count': [winners[0], winners[1], winners[2], winners[-1]]})
        elif num_players == 4:
            result = pd.DataFrame({'player': ['Player 1', 'Player 2', 'Player 3', 'Player 4', 'Draw'],
                                   'Win Count': [winners[0], winners[1], winners[2], winners[3], winners[-1]]})
        result['win_percent'] = result['Win Count'].map(lambda x: f"{round(x / games * 100, 2)}%")
        return result

    def make_win_chart(source):
        chart = alt.Chart(source).properties(height=350, width=700, title='Win Count(%) by player')
        win_chart = chart.mark_bar().encode(
            y='player',
            x='Win Count',
            color=alt.Color('player', scale=alt.Scale(scheme='dark2'))
        )
        text = win_chart.mark_text(
            align='left',
            baseline='middle',
            dx=3  # Nudges text to right so it doesn't appear on top of the bar
        ).encode(
            text='win_percent'
        )
        return win_chart + text

    st.altair_chart(make_win_chart(compile_win_percentages(num_players, data)))
    st.header('Number of rounds to complete game')
    st.write("""
    Shows how long a game would typically take.
    """)

    @st.cache
    def compile_rounds(rounds_series):
        rounds_container = [value for _, value in rounds_series.items()]
        rounds_counter = Counter(rounds_container)
        return pd.DataFrame({'Rounds': list(rounds_counter.keys()), 'count': list(rounds_counter.values())})

    def make_rounds_chart(source):
        base = alt.Chart(source).encode(
            x=alt.X('Rounds', bin=alt.Bin(step=5)),
        )
        rounds_bar = base.mark_bar().encode(
            y='count',
            color=alt.condition(alt.datum.Rounds > 300, alt.value('orange'), alt.value('slateblue'))
        ).properties(width=700, height=500)
        return rounds_bar

    st.altair_chart(make_rounds_chart(compile_rounds(data['rounds'])))
    st.header('Most visited spaces')
    st.write("""
    This shows you how often a place is visited during the 5 million games. 
    Wouldn't you consider trying for the hottest space?
    """)
    board_spaces = ['GO', 'CHANCE', 'JAIL', 'FREE PARKING', 'TACO TRUCK', 'PIZZA HOUSE', 'BAKERY',
                    'ICE CREAM PARLOUR',
                    'MUSEUM', 'LIBRARY', 'GO-KARTS', 'SWIMMING POOL', 'FERRIS WHEEL', 'ROLLER COASTER', 'TOY SHOP',
                    'PET SHOP',
                    'AQUARIUM', 'THE ZOO', 'PARK LANE', 'BOARDWALK']

    @st.cache
    def compile_spaces():
        visit_count = []
        for space in board_spaces:
            if space == 'CHANCE':
                visit_count.append(data[space].sum() / 4)
            else:
                visit_count.append(data[space].sum())
        return pd.DataFrame({'Space': board_spaces, 'Visit Count': visit_count})

    def make_visit_chart(source):
        visit_chart = alt.Chart(source).mark_bar().encode(
            x='Visit Count',
            y=alt.Y('Space:N', sort=board_spaces),
        ).properties(width=700, title='Spaces visited by players')
        rule = alt.Chart(source).mark_rule(color='red').encode(
            x='mean(Visit Count):Q'
        )
        return visit_chart + rule

    st.altair_chart(make_visit_chart(compile_spaces()))
    with st.beta_expander('Notes'):
        st.write(
            """
            * There are four CHANCE spaces in the board. The figure shown here is the visits in mean (total visits
              divided by 4).
            * The JAIL space includes landing on the JAIL space ("Just Visiting") or arriving via the GO TO JAIL space 
              or drawing the appropriate Chance Card.
            """)
