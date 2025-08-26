import itertools
from .scoring import score_word

class Computer:
    """
    Simple Computer to play Scrabble.
    Chooses the highest scoring word from its rack that fits on the board.
    """
    def __init__(self, game):
        self.game = game

    def find_anchors(self):
        """
        Find anchor points on the board (empty cells next to existing letters).
        Returns a list of (row, col) tuples.
        """
        anchors = []
        for r in range(15):
            for c in range(15):
                if self.game.board.grid[r][c]:
                    for dr, dc in [(-1,0),(1,0),(0,-1),(0,1)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < 15 and 0 <= nc < 15 and not self.game.board.grid[nr][nc]:
                            anchors.append((nr, nc))
        if not anchors:
            anchors = [(7, 7)]  # Center if board is empty
        return anchors

    # def play(self, player_rack, difficulty="HARD"):
    #     """
    #     Computer chooses the best move based on avComputerlable rack and board.
    #     Returns a tuple: (word, placement, score)
    #     """
    #     best_move = None
    #     best_score = 0
    #     anchors = self.find_anchors()

    #     for l in range(2, len(player_rack) + 1):
    #         for combo in set(itertools.permutations(player_rack, l)):
    #             word = "".join(combo)
    #             for anchor in anchors:
    #                 row, col = anchor
    #                 for direction in ["H", "V"]:
    #                     placement = self.game.board.place_word(word, row, col, direction, dry_run=True)
    #                     score = score_word(word, placement)
    #                     if score > best_score:
    #                         best_score = score
    #                         best_move = (word, placement)

    #     if best_move:
    #         word, placement = best_move
    #         self.game.board.place_word(word, placement["row"], placement["col"], placement["direction"])
    #         print(f"Computer played: {word} at ({placement['row']},{placement['col']}) {placement['direction']}, Score: {best_score}")
    #         return word, placement, best_score
    #     else:
    #         print("Computer cannot make a move")
    #         return None, None, 0

    def play(self, player_rack, difficulty="HARD"):
        best_move = None
        best_score = 0
        anchors = self.find_anchors()

        for l in range(2, len(player_rack) + 1):
            for combo in set(itertools.permutations(player_rack, l)):
                word = "".join(combo)
            for anchor in anchors:
                row, col = anchor
            for direction in ["H", "V"]:
                placement = self.game.board.place_word(word, row, col, direction, dry_run=True)

                    # Skip if placement was invalid (out of bounds)
            if placement is None:
                continue

            score = score_word(word, placement)
            if score > best_score:
                best_score = score
                best_move = (word, placement)

        if best_move:
            word, placement = best_move
            self.game.board.place_word(word, placement["row"], placement["col"], placement["direction"])
            print(f"Computer played: {word} at ({placement['row']},{placement['col']}) {placement['direction']}, Score: {best_score}")
            return word, placement, best_score
        else:
            print("Computer cannot make a move")
            return None, None, 0

