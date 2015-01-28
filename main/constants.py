from main.model.Position import Position

#For connection
PORT_NUMBER = 9998


#Positions and angles used in states
ANGLE_FOR_CARDINAL = {'S':0, 'SE':45, 'E':90, 'NE':135, 'N':180, 'NO':225, 'O':270, 'SO':315}
STARTING_ANGLE_FACING_PUCKS = 85
POSITION_TO_GO_MID_PUCKS = Position(173, 55.75)
POSITION_FACING_LETTER_BOARD = Position(173, 64)
POSITION_TO_GO_MID_SQUARE = Position(55, 55) 
POSITION_TO_GO_FOR_RESISTANCE_TRAY = Position(30,30)

#For GUI

COLOR_OF_PUCKS = ["BLACK","BROWN","RED","ORANGE","YELLOW","GREEN","BLUE","PURPLE","GREY","WHITE"]

ORIENTATION_POSITION_FOR_GUI = {1 : "742-270",
                2 : "814-260",
                3 : "875-260",
                4 : "750-322",
                5 : "814-322",
                6 : "869-331",
                7 : "742-393",
                8 : "807-393",
                9 : "869-393",
}

LETTER_POSITION_FOR_GUI = {1 : "488-260",
                2 : "552-260",
                3 : "612-260",
                4 : "488-321",
                5 : "552-321",
                6 : "612-321",
                7 : "488-385",
                8 : "552-385",
                9 : "612-385",
}


#For trajectory planner and map
NOTHING = 0
OBSTACLE = 9999
PUCK = 9998
GOAL = 1
ROBOT = 777
EXPAND = 999

RESET_MINIMUM_NODE = 666

LENGHT_TABLE = 230.0
WIDHT_TABLE = 113.8
CELL_EXPAND_CENTIMETER = 21
PUCK_EXPAND_CENTIMETER = 19
WALL_EXPAND_CENTIMETER = 15

