from classes import Color


class BoardSpace:
    def __init__(self, name: str, color: Color, price: int):
        self.name = name
        self.color = color
        self.price = price


BOARDWALK = 'BOARDWALK'

PARK_LANE = 'PARK LANE'

THE_ZOO = 'THE ZOO'

AQUARIUM = 'AQUARIUM'

GO_TO_JAIL = 'GO TO JAIL'

PET_SHOP = 'PET SHOP'

TOY_SHOP = 'TOY SHOP'

ROLLER_COASTER = 'ROLLER COASTER'

FERRIS_WHEEL = 'FERRIS WHEEL'

FREE_PARKING = 'FREE PARKING'

SWIMMING_POOL = 'SWIMMING POOL'

GO_KARTS = 'GO-KARTS'

LIBRARY = 'LIBRARY'

MUSEUM = 'MUSEUM'

JAIL = 'JAIL'

ICE_CREAM_PARLOUR = 'ICE CREAM PARLOUR'

BAKERY = 'BAKERY'

CHANCE = 'CHANCE'

PIZZA_HOUSE = 'PIZZA HOUSE'

TACO_TRUCK = 'TACO TRUCK'

GO = 'GO'

GO_Board_Space = BoardSpace(GO, Color.NA, 0)
TACO_TRUCK_Board_Space = BoardSpace(TACO_TRUCK, Color.BROWN, 1)
PIZZA_HOUSE_Board_Space = BoardSpace(PIZZA_HOUSE, Color.BROWN, 1)
Chance_Board_Space = BoardSpace(CHANCE, Color.CHANCE, 0)
BAKERY_Board_Space = BoardSpace(BAKERY, Color.LIGHT_BLUE, 1)
ICE_CREAM_PARLOUR_Board_Space = BoardSpace(ICE_CREAM_PARLOUR, Color.LIGHT_BLUE, 1)
JAIL_Board_Space = BoardSpace(JAIL, Color.NA, 0)
MUSEUM_Board_Space = BoardSpace(MUSEUM, Color.PINK, 2)
LIBRARY_Board_Space = BoardSpace(LIBRARY, Color.PINK, 2)
GO_KARTS_Board_Space = BoardSpace(GO_KARTS, Color.ORANGE, 2)
SWIMMING_POOL_Board_Space = BoardSpace(SWIMMING_POOL, Color.ORANGE, 2)
FREE_PARKING_Board_Space = BoardSpace(FREE_PARKING, Color.NA, 0)
FERRIS_WHEEL_Board_Space = BoardSpace(FERRIS_WHEEL, Color.RED, 3)
ROLLER_COASTER_Board_Space = BoardSpace(ROLLER_COASTER, Color.RED, 3)
TOY_SHOP_Board_Space = BoardSpace(TOY_SHOP, Color.YELLOW, 3)
PET_SHOP_Board_Space = BoardSpace(PET_SHOP, Color.YELLOW, 3)
GO_TO_JAIL_Board_Space = BoardSpace(GO_TO_JAIL, Color.NA, 0)
AQUARIUM_Board_Space = BoardSpace(AQUARIUM, Color.GREEN, 4)
ZOO_Board_Space = BoardSpace(THE_ZOO, Color.GREEN, 4)
PARK_LANE_Board_Space = BoardSpace(PARK_LANE, Color.DARK_BLUE, 5)
BOARDWALK_Board_Space = BoardSpace(BOARDWALK, Color.DARK_BLUE, 5)

game_board: [BoardSpace] = [
    GO_Board_Space,
    TACO_TRUCK_Board_Space,
    PIZZA_HOUSE_Board_Space,
    Chance_Board_Space,
    BAKERY_Board_Space,
    ICE_CREAM_PARLOUR_Board_Space,
    JAIL_Board_Space,
    MUSEUM_Board_Space,
    LIBRARY_Board_Space,
    Chance_Board_Space,
    GO_KARTS_Board_Space,
    SWIMMING_POOL_Board_Space,
    FREE_PARKING_Board_Space,
    FERRIS_WHEEL_Board_Space,
    ROLLER_COASTER_Board_Space,
    Chance_Board_Space,
    TOY_SHOP_Board_Space,
    PET_SHOP_Board_Space,
    GO_TO_JAIL_Board_Space,
    AQUARIUM_Board_Space,
    ZOO_Board_Space,
    Chance_Board_Space,
    PARK_LANE_Board_Space,
    BOARDWALK_Board_Space
]
