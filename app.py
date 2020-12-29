import streamlit as st

from game_explorer import game_explorer
from stat_explorer import stat_explorer

# Sidebar

GAME_EXPLORER = 'Game explorer'
STATISTICS_EXPLORER = 'Statistics explorer'

st.sidebar.title('Mpoly Junior Game simulation explorer')
st.sidebar.write("""
We ask a computer to play Mpoly Junior more than we will ever play in our lifetime.
The computer lets us in on some pretty fun insights in the game.
""")
num_players = st.sidebar.radio('Number of players', [2, 3, 4])
mode = st.sidebar.radio('Select Mode', [STATISTICS_EXPLORER, GAME_EXPLORER])
if mode == STATISTICS_EXPLORER:
    st.sidebar.write('Explorer the win percentages of each player, number of rounds it takes to complete the game '
                     'and space hotspots.')
elif mode == GAME_EXPLORER:
    st.sidebar.write('Pick a game and play through it for fun and curiosity.')

# Statistics explorer


if mode == STATISTICS_EXPLORER:
    stat_explorer(num_players)

# Game explorer


if mode == GAME_EXPLORER:
    game_explorer(num_players)
