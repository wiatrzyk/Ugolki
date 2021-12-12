from minmax import MinMax
import logging


class AI:
    @staticmethod
    def make_move(game, player=1):
        best_move = MinMax.find_move(game.board, player, 3)
        logging.info(f"AI move: {best_move}")
        game.move(best_move[0], best_move[1])
        if (game.turn % 2 == 0 and player == 1) or (game.turn % 2 == 1 and player == 2):
            game.next_turn()
        return game
