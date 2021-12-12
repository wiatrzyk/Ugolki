
class Game:
    def __init__(self):
        self.turn = 1
        self.board = [[0, 0, 0, 0, 2, 2, 2, 2],
                        [0, 0, 0, 0, 2, 2, 2, 2],
                        [0, 0, 0, 0, 2, 2, 2, 2],
                        [0, 0, 0, 0, 2, 2, 2, 2],
                        [1, 1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0],
                        [1, 1, 1, 1, 0, 0, 0, 0]]
        self.player1_score = 0
        self.player2_score = 0
        self.valid_moves = ['single_move', 'jump']
        self.possible_moves = []
        self.moves_coordinates = []

    @classmethod
    def from_board(cls, board, turn):
        o = cls()
        o.turn = turn
        o.board = board
        o.__update_players_score()
        return o

    def __update_players_score(self):
        count1, count2 = 0, 0
        for row in range(0, 4):
            for column in range(4, 8):
                if self.board[row][column] == 1:
                    count1 += 1
                if self.board[column][row] == 2:
                    count2 += 1
        self.player1_score = count1
        self.player2_score = count2

    def next_turn(self):
        self.turn += 1
        self.valid_moves = ['single_move', 'jump']
        self.moves_coordinates = []
        self.possible_moves = []

    def __check_valid_player(self, player):
        if self.turn % 2 == 0 and player == 1 or (self.turn % 2 == 1 and player == 2):
            return True
        return False

    def move(self, start_position, end_position):
        if self.__check_valid_move(start_position, end_position):
            player = self.board[start_position[0]][start_position[1]]
            if self.__check_valid_player(player):
                self.board[start_position[0]][start_position[1]] = 0
                self.board[end_position[0]][end_position[1]] = player

                x_dif = abs(start_position[0] - end_position[0])
                y_dif = abs(start_position[1] - end_position[1])
                if x_dif == 2 or y_dif == 2:
                    if self.__check_end_move(end_position):
                        self.next_turn()
                    else:
                        self.moves_coordinates.append(start_position)
                        self.possible_moves = self.find_possible_moves(end_position)
                        if not self.possible_moves:
                            self.next_turn()
                else:
                    self.next_turn()
            self.__update_players_score()
    
    def __check_possible_move(self, position, end_position):
        if self.__check_valid_move(position, end_position):
            if end_position not in self.moves_coordinates:
                return end_position

    def find_possible_moves(self, position):
        moves = []
        for i in [-2, -1, 1, 2]:
            move = self.__check_possible_move(position, [position[0] + i, position[1]])
            if move:
                moves.append(move)
            move = self.__check_possible_move(position, [position[0], position[1] + i])
            if move:
                moves.append(move)
        return moves

    def __check_valid_move(self, start_position, end_position) -> bool:
        for i in start_position:
            if i not in range(0, 8):
                return False
        for i in end_position:
            if i not in range(0, 8):
                return False

        if end_position in self.moves_coordinates:
            return False

        x_dif = abs(start_position[0] - end_position[0])
        y_dif = abs(start_position[1] - end_position[1])
        if x_dif == 0 and y_dif == 0:
            return False

        if self.board[end_position[0]][end_position[1]]:
            return False

        if abs(start_position[0] - end_position[0]) <= 2 and abs(start_position[1] - end_position[1]) <= 2:
            if x_dif == 0:
                if y_dif == 1:
                    if 'single_move' in self.valid_moves:
                        return True
                elif y_dif == 2:
                    if self.board[end_position[0]][end_position[1] - int((end_position[1] - start_position[1])/2)] != 0:
                        self.valid_moves = ['jump']
                        return True
            elif y_dif == 0:
                if x_dif == 1:
                    if 'single_move' in self.valid_moves:
                        return True
                elif x_dif == 2:
                    if self.board[end_position[0] - int((end_position[0] - start_position[0])/2)][end_position[1]] != 0:
                        self.valid_moves = ['jump']
                        return True
        return False

    @staticmethod
    def __next_move(coordinates, x, y):
        return [coordinates[0]+x, coordinates[1]+y]

    def __check_jump(self, end_position, x, y):
        """Checks if pawn can jump"""
        if x != 0:
            middle_x = x - 1 if x > 0 else x + 1
            middle_y = 0
        else:
            middle_x = 0
            middle_y = y - 1 if y > 0 else y + 1
        if not self.__check_valid_move(end_position, self.__next_move(end_position, middle_x, middle_y)) and \
                self.__check_valid_move(end_position, self.__next_move(end_position, x, y)):
            return True
        return False

    def __check_end_move(self, end_position) -> bool:
        """Checks if pawn can't jump further"""
        if self.__check_jump(end_position, 0, 2) or self.__check_jump(end_position, 0, -2) or \
                self.__check_jump(end_position, 2, 0) or self.__check_jump(end_position, -2, 0):
            return False
        return True

    def check_end(self):
        return self.player1_score == 16 or self.player2_score == 16
