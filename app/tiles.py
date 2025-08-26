from collections import Counter
import random

LETTER_COUNTS = {
    "A": 9, "B": 2, "C": 2, "D": 4, "E": 12,
    "F": 2, "G": 3, "H": 2, "I": 9, "J": 1,
    "K": 1, "L": 4, "M": 2, "N": 6, "O": 8,
    "P": 2, "Q": 1, "R": 6, "S": 4, "T": 6,
    "U": 4, "V": 2, "W": 2, "X": 1, "Y": 2,
    "Z": 1, "_": 2
}

LETTER_POINTS = {
    **{l: 1 for l in "EAIONRTLSU"},
    **{l: 2 for l in "DG"},
    **{l: 3 for l in "BCMP"},
    **{l: 4 for l in "FHVWY"},
    "K": 5,
    **{l: 8 for l in "JX"},
    **{l: 10 for l in "QZ"},
    "_": 0
}

class TileBag:
    def __init__(self, tiles=None):
        self.tiles = Counter(tiles or LETTER_COUNTS)

    def draw(self, n):
        pool = [l for l, c in self.tiles.items() for _ in range(c)]
        if n > len(pool):
            n = len(pool)
        random.shuffle(pool)
        picked = pool[:n]
        self.tiles.subtract(Counter(picked))
        self.tiles += Counter()  # Remove negatives
        return picked

    def put_back(self, letters):
        self.tiles.update(letters)

    def remaining(self):
        return dict(self.tiles)
