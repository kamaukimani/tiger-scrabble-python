import itertools
from .scoring import score_word
#from .game import end_game

class Computer:
  
    def __init__(self, game):
        self.game = game

    def find_anchors(self):
        #Find anchor points on the board (empty cells next to existing letters).
        #Returns a list of (row, col) tuples.
        
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

   
    def play(self, player_rack, difficulty="HARD"):
        best_move = None
        best_score = 0
        anchors = self.find_anchors()

        # Try words of length 2 up to full rack
        for l in range(2, len(player_rack) + 1):
            for combo in set(itertools.permutations(player_rack, l)):
                word = "".join(combo)

                # Skip if word  already played
                if word in self.game.played_words:
                    continue

                # Check if the word is valid
                if not self.game.dictionary.is_valid(word):
                    continue

                for anchor in anchors:
                    row, col = anchor
                    for direction in ["H", "V"]:
                        placement = self.game.board.place_word(word, row, col, direction, dry_run=True)

                        if placement is None:
                            continue  # Skip invalid placements

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
            self.game.end_game()   
            return None, None, 0

