import altair as alt
import pandas as pd
import streamlit as st

from board import game_board
from classes import get_token_name, WIN_RATE, POWER, POS, CASH, BANKRUPT, IN_JAIL, GET_OUT_OF_JAIL, CHANCE_MOVE, Color, \
    OWNER


def make_win_chart(selected_game, num_players):
    data_list = []
    player_list = [get_token_name(player) + WIN_RATE for player in range(num_players)] + ['draw_win%']
    source = selected_game.loc[:, player_list]
    for index, value in source.iterrows():
        for player in range(num_players):
            data_list.append(
                {'round': index, 'Winner': get_token_name(player),
                 'Win %': value[get_token_name(player) + WIN_RATE] * 100})
        data_list.append({'round': index, 'Winner': 'DRAW', 'Win %': value['draw_win%'] * 100})
    data = pd.DataFrame(data_list).fillna(0)
    win_chart = alt.Chart(data).mark_area().encode(
        x="round:O",
        y=alt.Y("Win %:Q"),
        color="Winner:N",
        tooltip=['round', 'Win %', 'Winner']
    ).properties(
        width=700,
        height=300
    )
    return win_chart


def make_power_chart(selected_game, num_players):
    data_list = []
    source = selected_game.loc[:, [get_token_name(player) + POWER for player in range(num_players)]]
    for index, value in source.iterrows():
        for player in range(num_players):
            data_list.append(
                {'round': index, 'Player': get_token_name(player),
                 'Power': value[get_token_name(player) + POWER]})
    data = pd.DataFrame(data_list).fillna(0)
    power_chart = alt.Chart(data).mark_line().encode(
        x="round:O",
        y="Power:Q",
        color='Player:N',
        tooltip=['round', 'Power', 'Player']
    ).properties(
        width=700,
        height=300
    )
    return power_chart


def get_player(player, current_round):
    player_name = get_token_name(player)
    if current_round[player_name + BANKRUPT]:
        data_list = {
            'Bankrupt': 'True',
        }
    else:
        data_list = {
            'Position': game_board[current_round[player_name + POS]].name,
            'Cash': current_round[player_name + CASH],
            'Bankrupt': current_round[player_name + BANKRUPT],
            'In Jail': current_round[player_name + IN_JAIL],
            'Jail Card': current_round[player_name + GET_OUT_OF_JAIL],
            'Chance Move': current_round[player_name + CHANCE_MOVE],
            'Win %': round(current_round[player_name + WIN_RATE] * 100, 2),
            'Power': current_round[player_name + POWER],
        }
    return pd.Series(data_list)


def game_explorer(num_players):
    st.title('Mpoly Junior Game game explorer')
    st.write("""
    Relive a game through a round by round account of the proceedings.

    * Select a game to load.
    * Scroll through the game by using the round controls.
    * Choose the number of players at the sidebar.

    """)

    with st.beta_expander('Notes'):
        st.write("""
        * Win% values are simulated based on playing 20,000 rounds with the same position.
        * Power ratings are calculated by sum of cash in hand and value of all property in the player's name.
        """)

    st.write("""
    ---
    """)
    st.header('Game Control')
    selected_game_no = st.number_input('Load Game #', 1, 15, value=1)

    @st.cache
    def load_game():
        game = pd.read_csv(f'game_data/{num_players}p/{selected_game_no}.csv')
        game.index.name = 'round'
        return game

    selected_game = load_game()
    st.write("""
    ---
    """)

    st.header('Round Control')
    selected_round_no = st.slider('Round', min_value=0, max_value=len(selected_game) - 1)
    st.write(f"The selected round is **#{selected_round_no}.**")
    st.write("You can use the arrow keys on your keyboard to move when this control is selected.")

    @st.cache
    def load_round():
        return selected_game.iloc[selected_round_no]

    current_round = load_round()
    st.write("""
    ---
    """)

    st.header('Game Board')

    st.subheader('Players')
    get_player_list(current_round, num_players)

    st.subheader('Notes')
    st.write(current_round['notes'])

    st.subheader('Board Spaces')
    board_spaces(current_round, num_players)

    st.subheader('Win% over the game')
    st.altair_chart(make_win_chart(selected_game, num_players))

    st.subheader('Power rating over the game')
    st.altair_chart(make_power_chart(selected_game, num_players))


def board_spaces(current_round, num_players):
    def get_row(i):
        for col in st.beta_columns(4):
            with col:
                st.write(f"**{game_board[i].name}**")
                if game_board[i].color not in [Color.NA, Color.CHANCE]:
                    st.write(f"Owner: {current_round[game_board[i].name + OWNER]}",
                             f"Price/Rent: {game_board[i].price}",
                             f"Color: {game_board[i].color}")
                players_pos = [get_token_name(player) for player in range(num_players) if
                               current_round[get_token_name(player) + POS] == i and not current_round[
                                   get_token_name(player) + BANKRUPT]]
                if len(players_pos) > 0:
                    st.write(f"Player(s) here: **{' '.join(players_pos)}**")
                i += 1
        return i

    i = 0
    i = get_row(i)
    i = get_row(i)
    i = get_row(i)
    i = get_row(i)
    i = get_row(i)
    get_row(i)


def get_player_list(current_round, num_players):
    col1, col2 = st.beta_columns(2)
    with col1:
        st.subheader('Player 1 - Little_T_REX')
        st.write(get_player(0, current_round))
    with col2:
        st.subheader('Player 2 - Little_Penguin')
        st.write(get_player(1, current_round))
    if num_players >= 3:
        col3, col4 = st.beta_columns(2)

        with col3:
            st.subheader('Player 3 - Little_Scottie')
            st.write(get_player(2, current_round))

        with col4:
            if num_players == 4:
                st.subheader('Player 4 - Little_Ducky')
                st.write(get_player(3, current_round))
