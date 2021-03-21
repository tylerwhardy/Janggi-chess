#  Author: Tyler W Hardy
#  Date: 27 Feb 2021
#  Description: Janggi game portfolio project. Instantiates a new game and allows the user to play.

if __name__ == "__main__":
    """
    Prevents activating code during doc builds
    """
    pass


def parse_color(name):
    """
    Function to determine color of a game-piece based on ID tag
    :param name: the name of the piece
    :return the player if one exists, False if not
    """
    if "R" in name:
        return "red"
    elif "B" in name:
        return "blue"
    else:
        return False


def generate_coordinate_grid():
    """
    Generates a coordinate grid for use in pruning legal moves
    :return a grid pattern representing the board
    """
    return [[x, y] for x in range(9) for y in range(10)]


def generate_fortress_grid():
    """
    Generates a coordinate grid for use in pruning legal moves in the fortress
    :return a grid pattern representing the fortresses on the board
    """
    loop_list_x = [3, 4, 5]
    loop_list_y = [0, 1, 2, 7, 8, 9]
    fortress_locations = []
    for j in loop_list_y:
        for i in loop_list_x:
            fortress_locations.append([i, j])
    return fortress_locations


class JanggiGame:
    """
    Instantiates a new game of Janggi
    """

    def __init__(self):
        """
        Creates starting conditions including populating the board
        """
        self._board = [["-"] * 9 for _ in range(10)]
        for j in range(10):
            if j < 3 or j > 6:
                self._board[j][3] = "-"
                self._board[j][4] = "-"
                self._board[j][5] = "-"
        self._game_state = "UNFINISHED"
        self._turn = "blue"
        self._general_list = []
        self._advisor_list = []
        self._horse_list = []
        self._elephant_list = []
        self._chariot_list = []
        self._cannon_list = []
        self._soldier_list = []
        self._check = None

        general_list = ["G_R_1", "G_B_1"]
        advisor_list = ["A_R_1", "A_R_2", "A_B_1", "A_B_2"]
        horse_list = ["H_R_1", "H_R_2", "H_B_1", "H_B_2"]
        elephant_list = ["E_R_1", "E_R_2", "E_B_1", "E_B_2"]
        chariot_list = ["C_R_1", "C_R_2", "C_B_1", "C_B_2"]
        cannon_list = ["K_R_1", "K_R_2", "K_B_1", "K_B_2"]
        soldier_list = ["S_R_1", "S_R_2", "S_R_3", "S_R_4", "S_R_5", "S_B_1", "S_B_2", "S_B_3", "S_B_4", "S_B_5"]

        for general in general_list:
            self._general_list.append(self.General(parse_color(general), general))
        for advisor in advisor_list:
            self._advisor_list.append(self.Advisor(parse_color(advisor), advisor))
        for horse in horse_list:
            self._horse_list.append(self.Horse(parse_color(horse), horse))
        for elephant in elephant_list:
            self._elephant_list.append(self.Elephant(parse_color(elephant), elephant))
        for chariot in chariot_list:
            self._chariot_list.append(self.Chariot(parse_color(chariot), chariot))
        for cannon in cannon_list:
            self._cannon_list.append(self.Cannon(parse_color(cannon), cannon))
        for soldier in soldier_list:
            self._soldier_list.append(self.Soldier(parse_color(soldier), soldier))
        self.place_pieces()
        self.draw_board()

    def get_general_list(self):
        """
        Gets General List
        :return private list of generals
        """
        return self._general_list

    def get_advisor_list(self):
        """
        Gets advisor list
        :return private list of advisors
        """
        return self._advisor_list

    def get_horse_list(self):
        """
        Gets horse list
        :return private list of horses
        """
        return self._horse_list

    def get_elephant_list(self):
        """
        Gets elephant list
        :return private list of elephants
        """
        return self._elephant_list

    def get_chariot_list(self):
        """
        Gets chariot list
        :return private list of chariots
        """
        return self._chariot_list

    def get_cannon_list(self):
        """
        Gets cannon list
        :return private list of cannons
        """
        return self._cannon_list

    def get_soldier_list(self):
        """
        Gets soldier list
        :return private list of soldiers
        """
        return self._soldier_list

    def get_check(self):
        """
        Gets the current player in check
        :return: player in check if one exists otherwise None
        """
        return self._check

    def get_game_state(self):
        """
        Gets game state
        :return current state of the game
        """
        return self._game_state

    def get_turn(self):
        """
        Gets the current turn
        :return current player turn
        """
        return self._turn

    def get_board(self):
        """
        Gets board
        :return current board object
        """
        return self._board

    def get_all_pieces(self):
        """
        Gets a list of lists of all pieces
        :return list of lists for all pieces on the board
        """
        return self.get_general_list(), self.get_advisor_list(), self.get_elephant_list(), self.get_chariot_list(), \
               self.get_horse_list(), self.get_cannon_list(), self.get_soldier_list()

    def set_check(self, color):
        """
        Sets a check flag for the impacted player
        :param color: the player receiving the check flag
        """
        self._check = color

    def set_game_state(self, state):
        """
        Sets game state to UNFINISHED or the color that won
        """
        self._game_state = state

    def remove_piece(self, identification, symbol):
        """
        Removes a captured piece from correct list through mutation
        :param identification: the ID code of the target
        :param symbol: the character representing a piece type
        """

        if symbol == "A":
            self._advisor_list.remove(identification)
        elif symbol == "H":
            self._horse_list.remove(identification)
        elif symbol == "E":
            self._elephant_list.remove(identification)
        elif symbol == "C":
            self._chariot_list.remove(identification)
        elif symbol == "K":
            self._cannon_list.remove(identification)
        elif symbol == "S":
            self._soldier_list.remove(identification)

    def change_turn(self):
        """
        Swaps the current turn between players.
        :return True on success, False on fail
        """
        if self.get_turn() == "blue":
            self._turn = "red"
            return True
        elif self.get_turn() == "red":
            self._turn = "blue"
            return True
        return False

    def place_pieces(self):
        """
        Places all pieces on the board by ID code
        """

        all_pieces = self.get_all_pieces()
        for type_of_item in all_pieces:
            for item in type_of_item:
                if item.get_id() == "G_R_1":
                    item.set_location(4, 1)
                elif item.get_id() == "G_B_1":
                    item.set_location(4, 8)
                elif item.get_id() == "A_R_1":
                    item.set_location(3, 0)
                elif item.get_id() == "A_R_2":
                    item.set_location(5, 0)
                elif item.get_id() == "A_B_1":
                    item.set_location(3, 9)
                elif item.get_id() == "A_B_2":
                    item.set_location(5, 9)
                elif item.get_id() == "H_R_1":
                    item.set_location(2, 0)
                elif item.get_id() == "H_R_2":
                    item.set_location(7, 0)
                elif item.get_id() == "H_B_1":
                    item.set_location(2, 9)
                elif item.get_id() == "H_B_2":
                    item.set_location(7, 9)
                elif item.get_id() == "E_R_1":
                    item.set_location(1, 0)
                elif item.get_id() == "E_R_2":
                    item.set_location(6, 0)
                elif item.get_id() == "E_B_1":
                    item.set_location(1, 9)
                elif item.get_id() == "E_B_2":
                    item.set_location(6, 9)
                elif item.get_id() == "C_R_1":
                    item.set_location(0, 0)
                elif item.get_id() == "C_R_2":
                    item.set_location(8, 0)
                elif item.get_id() == "C_B_1":
                    item.set_location(0, 9)
                elif item.get_id() == "C_B_2":
                    item.set_location(8, 9)
                elif item.get_id() == "K_R_1":
                    item.set_location(1, 2)
                elif item.get_id() == "K_R_2":
                    item.set_location(7, 2)
                elif item.get_id() == "K_B_1":
                    item.set_location(1, 7)
                elif item.get_id() == "K_B_2":
                    item.set_location(7, 7)
                elif item.get_id() == "S_R_1":
                    item.set_location(0, 3)
                elif item.get_id() == "S_R_2":
                    item.set_location(2, 3)
                elif item.get_id() == "S_R_3":
                    item.set_location(4, 3)
                elif item.get_id() == "S_R_4":
                    item.set_location(6, 3)
                elif item.get_id() == "S_R_5":
                    item.set_location(8, 3)
                elif item.get_id() == "S_B_1":
                    item.set_location(0, 6)
                elif item.get_id() == "S_B_2":
                    item.set_location(2, 6)
                elif item.get_id() == "S_B_3":
                    item.set_location(4, 6)
                elif item.get_id() == "S_B_4":
                    item.set_location(6, 6)
                elif item.get_id() == "S_B_5":
                    item.set_location(8, 6)
                item.check_in_fortress()

    def draw_board(self):
        """
        Prints blank board state for debugging
        """
        self._board = [["     "] * 9 for _ in range(10)]
        for j in range(10):
            if j < 3 or j > 6:
                self._board[j][3] = "-----"
                self._board[j][4] = "-----"
                self._board[j][5] = "-----"

        all_pieces = self.get_all_pieces()

        for type_of_item in all_pieces:
            for item in type_of_item:
                loc = item.get_location()
                loc_x = loc[0]
                loc_y = loc[1]
                symbol = item.get_id()
                self._board[loc_y][loc_x] = symbol  # Rotation required to make it fit in console
        for i in self.get_board():
            print(i)

    def draw_piece(self, piece):
        """
        Provides information on location and symbol of a game-piece
        :param: piece: the object representing the piece
        :return piece.get_symbol, the symbol representing the type of piece
        :return piece.get_location, the current coordinates the piece is located
        """
        return piece.get_symbol(), piece.get_location()

    def check_if_in_check(self, attack_space, board, type_of_mover):
        """
        This determines if a general has been placed in check
        :return True if in check, False if not
        """
        general_list = self.get_general_list()
        general_loc = []
        general_obj = None
        if self.get_turn() == "blue":
            for general in general_list:
                if general.get_color() == "red":
                    general_loc = general.get_location()
                    general_obj = general
        elif self.get_turn() == "red":
            for general in general_list:
                if general.get_color() == "blue":
                    general_loc = general.get_location()
                    general_obj = general
        for location in attack_space:
            if location == general_loc:
                print(type_of_mover)
                collisions = JanggiGame.Mobile.check_collision(None, location, general_loc, board, type_of_mover)
                if type_of_mover == "K" and collisions != 1:
                    return False
                if type_of_mover == "C" and collisions > 0:
                    return False
                if type_of_mover == "H" and collisions > 0:
                    return False
                self.set_check(general_obj.get_color())
                print("CHECK!")
                self.check_if_in_mate(general_obj)
                return True
            else:
                self.set_check(None)
                print("Not check")
        self.check_if_in_mate(general_obj)

    def attack_space(self, general):
        """
        Collects a list of areas under enemy threat
        :param: general: an object representing turn's general
        :return: attacker_legal: list of squares that could be attacked next turn"""
        master_list = self.get_all_pieces()
        attacker_list = []
        attacker_legal = []

        for type_piece in master_list:
            for piece in type_piece:
                if piece.get_color() != general.get_color():
                    attacker_list.append(piece)
        for attacker in attacker_list:
            attacker_legal.append(attacker.get_legal_moves(attacker.get_location()))
        return attacker_legal

    def check_if_in_mate(self, general):
        """
        Determines if a general is in checkmate.
        :return True if in checkmate, False if not.
        """
        master_list = self.get_all_pieces()
        attacker_list = []
        attacker_legal = []

        for type_piece in master_list:
            for piece in type_piece:
                if piece.get_color() != general.get_color():
                    attacker_list.append(piece)
        for attacker in attacker_list:
            attacker_legal.append(attacker.get_legal_moves(attacker.get_location()))
        general_legal = general.get_legal_moves(general.get_location())
        for gen_move in general_legal:
            if gen_move in attacker_legal:
                general_legal.remove(gen_move)
        if len(general_legal) == 0:
            self.set_game_state(general.get_color.upper() + "_WON")
        return False

    class Mobile:
        """Defines mobile objects within the game"""

        def __init__(self, color, identification):
            """
            Initializes mobile objects
            :param color: the player that owns the new piece
            :param identification: the ID code of the piece
            """
            self._legal_moves = None
            self._legal_moves_fortress = None
            self._color = color
            self._location = None, None
            self._id = identification
            self._symbol = None
            self._inside_fortress = False

        def get_color(self):
            """
            Gets color
            :return private data color
            """
            return self._color

        def get_symbol(self):
            """
            Gets the symbol of the piece
            :return private data symbol
            """
            return self._symbol

        def get_location(self):
            """
            Gets location
            :return private data location
            """
            return self._location

        def get_id(self):
            """
            Gets ID
            :return private data ID code
            """
            return self._id

        def get_in_fortress(self):
            """
            Gets the status of being in the fortress
            :return private data boolean inside_fortress"""
            return self._inside_fortress

        def get_legal_moves(self, current_loc):
            """
            Returns legal moves of a piece
            :return list of coordinates that are legal, parsed for being on board
            """
            move_potential = []
            move_approved = []
            if self.get_in_fortress() is True:
                moves = self._legal_moves_fortress
                if self.get_symbol() != "G" or self.get_symbol() != "A":
                    board_grid = generate_coordinate_grid()
                else:
                    board_grid = generate_fortress_grid()
            else:
                moves = self._legal_moves
                board_grid = generate_coordinate_grid()
            for move in moves:
                move_potential.append([current_loc[0] + move[0], current_loc[1] + move[1]])
            for square in board_grid:
                for coord in move_potential:
                    if coord == square:
                        move_approved.append(coord)
            return move_approved

        def set_location(self, location_x, location_y):
            """
            Sets location of the piece using inputs
            :param location_x: the x coordinate
            :param location_y: the y coordinate
            """
            self._location = [location_x, location_y]

        def set_in_fortress(self):
            """
            Sets the piece to be in the fortress
            """
            self._inside_fortress = True

        def set_out_fortress(self):
            """
            Sets the piece to be outside the fortress
            """
            self._inside_fortress = False

        def check_in_fortress(self):
            """
            Checks to see if piece is in fortress
            """
            fortress_locations = generate_fortress_grid()
            if self.get_location() in fortress_locations:
                self.set_in_fortress()
            else:
                self.set_out_fortress()

        def check_collision(self, start_loc, end_loc, board, type_of_mover):
            """
            Counts collisions between starting and ending locations
            :param type_of_mover: Character symbol representing the class of piece
            :param start_loc: the starting location
            :param end_loc: the ending location
            :param board: an list of all occupied squares
            :return: collision_total: count of collision risks
            """
            collision_total = 0
            step_x = 1
            step_y = 1
            test_coord_col = 0
            delta_x = start_loc[0] - end_loc[0]
            delta_y = start_loc[1] - end_loc[1]
            if delta_x < 0:
                step_x = -1
            if delta_y < 0:
                step_y = -1

            collision_list = []
            for type_piece in board:
                for piece in type_piece:
                    collider_loc = piece.get_location()
                    if collider_loc != start_loc and collider_loc != end_loc:
                        collision_list.append(collider_loc)
            if type_of_mover == "C" or type_of_mover == "K":
                if delta_x == 0:
                    for n_y in range(0, delta_y, step_y):
                        test_coord_col = [start_loc[0], start_loc[1] - n_y]
                        if test_coord_col in collision_list:
                            collision_total += 1
                if delta_y == 0:
                    for n_x in range(0, delta_x, step_x):
                        test_coord_col = [start_loc[0] - n_x, start_loc[1]]
                        if test_coord_col in collision_list:
                            collision_total += 1

            if type_of_mover == "H":
                delta_x = - delta_x  # Added to fix board shift
                delta_y = - delta_y
                if delta_x == 0 and delta_y == 0:
                    return 0
                if delta_x == 1:
                    if delta_y == 2:  # 1,2
                        test_coord_col = [start_loc[0], start_loc[1] + 1]
                    if delta_y == -2:  # 1,-2
                        test_coord_col = [start_loc[0], start_loc[1] - 1]
                if delta_x == 2:
                    if delta_y == 1:  # 2,1
                        test_coord_col = [start_loc[0] + 1, start_loc[1]]
                    if delta_y == -1:  # 2,-1
                        test_coord_col = [start_loc[0] - 1, start_loc[1]]
                if delta_x == -1:
                    if delta_y == 2:  # -1, 2
                        test_coord_col = [start_loc[0], start_loc[1] + 1]
                    if delta_y == -2:  # -1,-2
                        test_coord_col = [start_loc[0], start_loc[1] - 1]
                if delta_x == -2:
                    if delta_y == 1:  # -2,1
                        test_coord_col = [start_loc[0] - 1, start_loc[1]]
                    if delta_y == -1:  # -2,-1
                        test_coord_col = [start_loc[0] + 1, start_loc[1] + - 1]
                if test_coord_col in collision_list:
                    collision_total += 1

            if type_of_mover == "E":  # Need to verify vals
                delta_x = - delta_x  # Added to fix board shift
                delta_y = - delta_y
                if delta_x == 0 and delta_y == 0:
                    return 0
                if delta_x == 2:
                    if delta_y == 3:  # 1,2
                        test_coord_col = [start_loc[0], start_loc[1] + 1]
                    if delta_y == -3:  # 1,-2
                        test_coord_col = [start_loc[0], start_loc[1] - 1]
                if delta_x == 3:
                    if delta_y == 2:  # 2,1
                        test_coord_col = [start_loc[0] + 1, start_loc[1]]
                    if delta_y == -2:  # 2,-1
                        test_coord_col = [start_loc[0] - 1, start_loc[1]]
                if delta_x == -2:
                    if delta_y == 3:  # -1, 2
                        test_coord_col = [start_loc[0], start_loc[1] + 1]
                    if delta_y == -3:  # -1,-2
                        test_coord_col = [start_loc[0], start_loc[1] - 1]
                if delta_x == -3:
                    if delta_y == 2:  # -2,1
                        test_coord_col = [start_loc[0] - 1, start_loc[1]]
                    if delta_y == -2:  # -2,-1
                        test_coord_col = [start_loc[0] + 1, start_loc[1] + - 1]
                if test_coord_col in collision_list:
                    collision_total += 1
            return collision_total

    class Soldier(Mobile):
        """
        Class for Soldier. Inherits from Mobile. Can move 1 space forward or one space horizontal. 5 per game
        If enters fortress, can now move diagonal
        """

        def __init__(self, color, ident):
            """
            Initializes the Soldier class
            :param color: the player that owns the soldier
            :param ident: the ID tag of the soldier
            """
            super().__init__(color, ident)
            self._symbol = "S"
            if self.get_color() == "red":
                self._legal_moves = [[0, 0], [1, 0], [-1, 0], [0, 1]]
                self._legal_moves_fortress = [[0, 0], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0],
                                              [-1, 1]]
            elif self.get_color() == "blue":
                self._legal_moves = [[0, 0], [1, 0], [-1, 0], [0, -1]]
                self._legal_moves_fortress = [[0, 0], [0, -1], [1, 0], [-1, 0], [1, 1], [-1, -1], [-1, -1], [1, 1],
                                              [0, 1]]

    class Cannon(Mobile):
        """Class for Cannon. Inherits from Mobile"""

        def __init__(self, color, ident):
            """
            Initializes the Cannon class
            :param color: the player that owns the cannon
            :param ident: the ID tag of the cannon
            """
            super().__init__(color, ident)
            self._symbol = "K"
            self._legal_moves = []
            cardinal_moves = [[0, 0], [0, 1], [1, 0], [-1, 0], [0, -1]]
            for i in range(1, 9):
                for coord in cardinal_moves:
                    self._legal_moves.append([coord[0], coord[1] * i])
                    self._legal_moves.append([coord[0] * i, coord[1]])
                    self._legal_moves.append([coord[0] * i, coord[1] * i])
            self._legal_moves_fortress = [[0, 0], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    class Chariot(Mobile):
        """Class for Chariot. Inherits from Mobile. May move orthogonally any distance and diagonally inside the
        fortress. """

        def __init__(self, color, ident):
            """
            Initializes the Chariot class
            :param color: the player that owns the chariot
            :param ident: the ID tag of the chariot
            """
            super().__init__(color, ident)
            self._symbol = "C"
            self._legal_moves = []
            cardinal_moves = [[0, 0], [0, 1], [1, 0], [0, -1], [-1, 0]]
            for i in range(1, 9):
                for coord in cardinal_moves:
                    self._legal_moves.append([coord[0], coord[1] * i])
                    self._legal_moves.append([coord[0] * i, coord[1]])

                    # self._legal_moves.append([coord[0] + i, coord[1] * i])
            self._legal_moves_fortress = [[0, 0], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]

    class Horse(Mobile):
        """Class for Horse. Inherits from Mobile. Horses may move one diagonal/vertical space and one diagonal space
        Horses may not move through blocked spaces."""

        def __init__(self, color, ident):
            """
            Initializes the Horse class
            :param color: the player that owns the horse
            :param ident: the ID tag of the horse
            """
            super().__init__(color, ident)
            self._symbol = "H"
            self._legal_moves = [[0, 0], [1, 2], [2, 1], [-1, 2], [-2, 1], [1, -2], [2, -1], [-1, -2], [-2, -1]]
            self._legal_moves_fortress = self._legal_moves

    class Elephant(Mobile):
        """Class for Elephant. Inherits from Mobile."""

        def __init__(self, color, ident):
            """
            Initializes the Elephant class
            :param color: the player that owns the elephant
            :param ident: the ID tag of the elephant
            """
            super().__init__(color, ident)
            self._symbol = "E"
            self._legal_moves = [[0, 0], [2, 3], [3, 2], [-2, 3], [-3, 2], [2, -3], [3, -2], [-2, -3], [-3, -2]]
            self._legal_moves_fortress = self._legal_moves

    class Advisor(Mobile):
        """Class for Advisor. Inherits from Mobile. Advisors must stay in the fortress and may move in any direction
        one square at a time"""

        def __init__(self, color, ident):
            """
            Initializes the Advisor class
            :param color: the player that owns the advisor
            :param ident: the ID tag of the advisor
            """
            super().__init__(color, ident)
            self._symbol = "A"
            self._legal_moves = [[0, 0], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            self._legal_moves_fortress = self._legal_moves

    class General(Mobile):
        """Class for General. Inherits from Mobile. Can move 1 space in any direction but may never leave fortress.
        Generals may never directly face either other without an intervening piece. To do so is to cause a draw"""

        def __init__(self, color, ident):
            """
            Initializes the General class
            :param color: the player that owns the general
            :param ident: the ID tag of the general
            """
            super().__init__(color, ident)
            self._symbol = "G"
            self._legal_moves = [[0, 0], [0, 1], [1, 1], [1, 0], [1, -1], [0, -1], [-1, -1], [-1, 0], [-1, 1]]
            self._legal_moves_fortress = self._legal_moves

    def find_from_loc(self, x, y):
        """
        Finds a piece at a given coordinate
        :param x: the x coordinate to search
        :param y: the y coordinate to search
        :return: the piece object if one is found, False if not
        """
        search_list = self.get_all_pieces()
        for types in search_list:
            for piece in types:
                if piece.get_location() == [x, y]:
                    return piece
        return False

    def make_move(self, move_from, move_to):
        """
        Moves a piece in spatial coordinates
        :param move_from: the coordinates moving from
        :param move_to: the coordinates moving to
        :return: True if successful, False if not
        """
        print("*" * 100)
        print("Starting to move!")
        if self.get_game_state() != "UNFINISHED":  # Prevents moving after checkmate
            return False
        if self.get_check() == self.get_turn():
            am_i_in_check = True
        am_i_in_check = False # Flag for checking if you're starting the turn in check
        start_x = int(ord(move_from[0]) - 97)
        start_y = int(move_from[1:]) - 1
        end_x = int(ord(move_to[0]) - 97)
        end_y = int(move_to[1:]) - 1
        mover = self.find_from_loc(start_x, start_y)
        if mover:
            print(mover.get_id(), " wants to move from: ", mover.get_location(), " to ", [end_x, end_y])
            current_loc = mover.get_location()
            legal_moves = mover.get_legal_moves(current_loc)
            for move in legal_moves:
                if [move[0], move[1]] == [end_x, end_y]:
                    if mover.get_color() == self.get_turn():
                        target_mob = self.find_from_loc(end_x, end_y)
                        collisions = mover.check_collision(current_loc, [end_x, end_y], self.get_all_pieces(),
                                                           mover.get_symbol())
                        print("Collisions:", collisions)
                        if mover.get_symbol() == "K" and collisions != 1:
                            return False
                        if mover.get_symbol() == "C" and collisions > 0:
                            return False
                        if mover.get_symbol() == "H" and collisions > 0:
                            return False
                        if mover.get_symbol() == "G" and self.check_if_in_check(self.attack_space(mover),
                                                                                self.get_all_pieces(), "G") is True:
                            return False
                        if target_mob:
                            if target_mob.get_color() == self.get_turn() and target_mob != mover:
                                return False
                            if target_mob != mover:
                                print("Captured piece! ", target_mob.get_id(), " will be removed.")
                                self.remove_piece(target_mob, target_mob.get_symbol())

                        mover.set_location(end_x, end_y)
                        check_state = self.check_if_in_check(self.attack_space(mover), self.get_all_pieces(), "G")
                        if check_state and am_i_in_check:  # Failed to counter check
                            mover.set_location(start_x, start_y)
                            return False
                        mover.check_in_fortress()
                        self.draw_board()
                        current_loc = mover.get_location()
                        check_risk = mover.get_legal_moves(current_loc)
                        self.check_if_in_check(check_risk, self.get_all_pieces(), mover.get_symbol())
                        self.change_turn()
                        print("Turn Complete. Turn belongs to: ", self.get_turn())
                        return True
        print("Move failed due to an error\n")
        return False

    def is_in_check(self, player):
        """
        Returns if a player is in check by calling the respective check function
        param: player: the owner to check
        :return True if in check, False if not
        """
        if player == "blue" and self.get_check() == "blue":
            return True
        if player == "red" and self.get_check() == "red":
            return True
        return False
