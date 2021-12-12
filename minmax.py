from random import choice
from game import Game
from copy import deepcopy
import logging


def log_board(board, score, score2):
    new_list = list(map(str, zip(*board)))
    logging.debug("\n".join([str(score) + " " + str(score2), *new_list]))


class TreeNode:
    def __init__(self, board, player, level, max_level=1, parent=None, move=None):
        self.current_board = board.copy()
        self.player = player
        self.value = 0
        self.parent = parent
        self.level = level
        self.max_level = max_level
        self.move = move
        self.children = []
        self.game = Game.from_board(board.copy(), player)
        if level < max_level:
            self.insert_children()

    def find_pawns_coordinates(self) -> list:
        pawns_coordinates = []
        for row in range(0, 8):
            for column in range(0, 8):
                if self.current_board[row][column] == self.player:
                    pawns_coordinates.append([row, column])
        return pawns_coordinates

    def find_all_moves(self):
        moves = []
        pawns_coordinates = self.find_pawns_coordinates()
        for coordinates in pawns_coordinates:
            self.game.valid_moves = ['single_move', 'jump']
            moves_coordinates = self.game.find_possible_moves(coordinates)
            for move in moves_coordinates:
                moves.append([coordinates, move])
        return moves

    def insert_children(self):
        all_moves = self.find_all_moves()
        for move in all_moves:
            board_new = deepcopy(self.current_board)
            start_position = move[0]
            end_position = move[1]
            board_new[start_position[0]][start_position[1]] = 0
            board_new[end_position[0]][end_position[1]] = self.player
            next_player = 1 if self.player == 2 else 2
            new_node = TreeNode(board_new, next_player, self.level + 1, self.max_level, self, move)
            self.children.append(new_node)


class MinMax:
    @staticmethod
    def minmax_alphabeta(node, depth, max_player, alpha=-10000, beta=10000):
        if depth == 0 or node.children == []:
            node.value = MinMax.evaluate_points(node.current_board)
            return node.value

        if max_player:
            max_eval = -10000
            for child in node.children:
                val = MinMax.minmax_alphabeta(child, depth - 1, not max_player, alpha, beta)
                max_eval = max(max_eval, val)
                alpha = max(alpha, val)
                if beta <= alpha:
                    break
            return max_eval
        else:
            min_eval = 10000
            for child in node.children:
                val = MinMax.minmax_alphabeta(child, depth - 1, not max_player, alpha, beta)
                min_eval = min(min_eval, val)
                beta = min(beta, val)
                if beta <= alpha:
                    break
            return min_eval

    @staticmethod
    def find_move(board, player, max_lvl) -> list:
        root = TreeNode(board, player, 0, max_lvl)
        if player == 1:
            for node in root.children:
                node.value = MinMax.minmax_alphabeta(node, max_lvl, False)
            children_values = [node.value for node in root.children]
            value = max(children_values)
        else:
            for node in root.children:
                node.value = MinMax.minmax_alphabeta(node, max_lvl, True)
                children_values = [node.value for node in root.children]
                value = min(children_values)

        moves = []
        for child in root.children:
            if value == child.value:
                moves.append(child.move)
        return choice(moves) if moves else []

    @staticmethod
    def find_nodes(node, current_lvl, requested_lvl, results):
        if current_lvl == requested_lvl:
            results.append(node)
            return results
        else:
            for child in node.children:
                results = MinMax.find_nodes(child, current_lvl + 1, requested_lvl, results)
            return results

    @staticmethod
    def evaluate_points(board):
        player1_score, player2_score = 0, 0
        for row in range(0, 4):
            for column in range(4, 8):
                if board[row][column] == 1:
                    player1_score += 100
                if board[column][row] == 2:
                    player2_score += 100

        for row in range(0, 8):
            for column in range(0, 8):
                if board[column][row] == 1:
                    val1 = (8 if row >= 5 else 8 - row) * 3
                    val2 = (8 if column <= 2 else 8 - column) * 3
                    value = val1 + val2
                    player1_score += value

                elif board[column][row] == 2:
                    val1 = (8 if row <= 2 else 8 - row) * 3
                    val2 = (8 if column >= 5 else 8 - column) * 3
                    value = val1 + val2
                    player2_score += value

        # log_board(board, player1_score, player2_score)
        return player1_score - player2_score
