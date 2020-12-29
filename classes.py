from enum import Enum

WIN_RATE = '_win%'
POWER = '_power'
BANKRUPT = '_bankrupt'
CHANCE_MOVE = '_chance_move'
GET_OUT_OF_JAIL = '_get_out_of_jail'
OWNER = '_owner'
IN_JAIL = '_in_jail'
POS = "_pos"
CASH = '_cash'


def get_token_name(i: int) -> str:
    return TokenCharacter(i).name


class TokenCharacter(Enum):
    Little_T_REX = 0
    Little_Penguin = 1
    Little_Scottie = 2
    Little_Ducky = 3

    def __str__(self):
        return self.name


class Color(Enum):
    NA = 0
    BROWN = 1
    LIGHT_BLUE = 2
    PINK = 3
    ORANGE = 4
    RED = 5
    YELLOW = 6
    GREEN = 7
    DARK_BLUE = 8,
    CHANCE = 9
