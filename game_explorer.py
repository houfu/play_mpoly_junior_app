import altair as alt
import pandas as pd
import streamlit as st
from numpy import nan

from board import game_board, JAIL
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
                    owner = current_round[game_board[i].name + OWNER] if current_round[
                                                                             game_board[
                                                                                 i].name + OWNER] is not nan else 'BANK'
                    st.write(
                        f"Owner: {owner}",
                        f"Price/Rent: {game_board[i].price}",
                        f"Color: {game_board[i].color}")
                players_pos = [get_token_name(player) for player in range(num_players) if
                               current_round[get_token_name(player) + POS] == i and not current_round[
                                   get_token_name(player) + BANKRUPT]]
                if len(players_pos) > 0:
                    if game_board[i].name == JAIL:
                        players_pos = [
                            player_pos + " (In Jail)" if current_round[
                                player_pos + IN_JAIL] else player_pos + ' (Just visiting)'
                            for player_pos in players_pos]
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
    def get_player(current_player: int):
        player_name = get_token_name(current_player)
        col1, col2, col3 = st.beta_columns([1, 1, 4])
        with col1:
            st.subheader(f'**Player {current_player + 1} - {player_name}**')
        with col2:
            st.image(f"{player_name}.gif", use_column_width=True)
        with col3:
            if current_round[player_name + BANKRUPT]:
                data_list = {
                    'Position': game_board[current_round[player_name + POS]].name,
                    'Bankrupt': 'True',
                }
            else:
                position = game_board[current_round[player_name + POS]].name
                if position == JAIL:
                    position = position + " (In Jail)" if current_round[
                        player_name + IN_JAIL] else position + ' (Just visiting)'
                data_list = {
                    'Position': position,
                    'Cash': current_round[player_name + CASH],
                }
                if current_round[player_name + GET_OUT_OF_JAIL]:
                    data_list.update({'Jail Card': True})
                if current_round[player_name + CHANCE_MOVE]:
                    data_list.update({'Chance Move': True})
                data_list.update({
                    'Win %': round(current_round[player_name + WIN_RATE] * 100, 2),
                    'Power': current_round[player_name + POWER],
                })
            st.write(pd.Series(data_list))

    for player in range(num_players):
        get_player(player)
