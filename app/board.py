from typing import Optional

MULTIPLIER_LAYOUT = [
    ["TW", None, None, "DL", None, None, None, "TW", None, None, None, "DL", None, None, "TW"],
    [None, "DW", None, None, None, "TL", None, None, None, "TL", None, None, None, "DW", None],
    [None, None, "DW", None, None, None, "DL", None, "DL", None, None, None, "DW", None, None],
    ["DL", None, None, "DW", None, None, None, "DL", None, None, None, "DW", None, None, "DL"],
    [None, None, None, None, "DW", None, None, None, None, None, "DW", None, None, None, None],
    [None, "TL", None, None, None, "TL", None, None, None, "TL", None, None, None, "TL", None],
    [None, None, "DL", None, None, None, "DL", None, "DL", None, None, None, "DL", None, None],
    ["TW", None, None, "DL", None, None, None, "DW", None, None, None, "DL", None, None, "TW"],
    [None, None, "DL", None, None, None, "DL", None, "DL", None, None, None, "DL", None, None],
    [None, "TL", None, None, None, "TL", None, None, None, "TL", None, None, None, "TL", None],
    [None, None, None, None, "DW", None, None, None, None, None, "DW", None, None, None, None],
    ["DL", None, None, "DW", None, None, None, "DL", None, None, None, "DW", None, None, "DL"],
    [None, None, "DW", None, None, None, "DL", None, "DL", None, None, None, "DW", None, None],
    [None, "DW", None, None, None, "TL", None, None, None, "TL", None, None, None, "DW", None],
    ["TW", None, None, "DL", None, None, None, "TW", None, None, None, "DL", None, None, "TW"],
]

class Board:
    def __init__(self):
        # 15x15 empty board
        self.grid: list[list[Optional[str]]] = [[None] * 15 for _ in range(15)]

    # def place_word(self, word, row, col, direction, dry_run=False):

    #     word = word.upper()
    #     letter_multipliers = []
    #     word_multiplier = 1

    #     for i, ch in enumerate(word):
    #         r, c = (row, col + i) if direction == "H" else (row + i, col)

            
    #         if self.grid[r][c] is None and not dry_run:
    #             self.grid[r][c] = ch

    #         mult = MULTIPLIER_LAYOUT[r][c]
    #         if mult == "DL":
    #             letter_multipliers.append(2)
    #         elif mult == "TL":
    #             letter_multipliers.append(3)
    #         else:
    #             letter_multipliers.append(1)

    #         if mult == "DW":
    #             word_multiplier *= 2
    #         elif mult == "TW":
    #             word_multiplier *= 3

    #     return {
    #         "row": row,
    #         "col": col,
    #         "direction": direction,
    #         "letter_multipliers": letter_multipliers,
    #         "word_multiplier": word_multiplier,
    #     }


    #...............occupied tile conflict..............
    # def place_word(self, word, row, col, direction, dry_run=False):
    #     word = word.upper()
    #     letter_multipliers = []
    #     word_multiplier = 1
   

    #     for i, ch in enumerate(word):
    #         r, c = (row, col + i) if direction == "H" else (row + i, col)

    #     # Prevent out-of-bounds errors
    #         if not (0 <= r < 15 and 0 <= c < 15):
    #             if dry_run:
    #                 return None  # Signal invalid placement
    #             else:
    #                 raise ValueError(f"Out of bounds: trying to place '{word}' at ({r}, {c})")

    #         if self.grid[r][c] is None and not dry_run:
    #             self.grid[r][c] = ch

    #         mult = MULTIPLIER_LAYOUT[r][c]
    #         if mult == "DL":
    #             letter_multipliers.append(2)
    #         elif mult == "TL":
    #             letter_multipliers.append(3)
    #         else:
    #             letter_multipliers.append(1)

    #         if mult == "DW":
    #             word_multiplier *= 2
    #         elif mult == "TW":
    #          word_multiplier *= 3

    #     return {
    #     "row": row,
    #     "col": col,
    #     "direction": direction,
    #     "letter_multipliers": letter_multipliers,
    #     "word_multiplier": word_multiplier,
    #     }

#...............occupied tile conflict..............


#...............ensure they are connected and start at centre......
    # def place_word(self, word, row, col, direction, dry_run=False):
    #     word = word.upper()
    #     letter_multipliers = []
    #     word_multiplier = 1

    #     for i, ch in enumerate(word):
    #         r, c = (row, col + i) if direction == "H" else (row + i, col)

    #         # Bounds check
    #         if not (0 <= r < 15 and 0 <= c < 15):
    #             if dry_run:
    #                 return None
    #             else:
    #                 raise ValueError(f"Out of bounds: trying to place '{word}' at ({r}, {c})")

    #         board_letter = self.grid[r][c]

    #         #  Check for conflict
    #         if board_letter and board_letter != ch:
    #             if dry_run:
    #                 return None
    #             else:
    #                 raise ValueError(
    #                     f"Conflict at ({r}, {c}): board has '{board_letter}', but trying to place '{ch}'"
    #                 )

    #         if not board_letter and not dry_run:
    #             self.grid[r][c] = ch

    #         mult = MULTIPLIER_LAYOUT[r][c]
    #         if mult == "DL":
    #             letter_multipliers.append(2)
    #         elif mult == "TL":
    #             letter_multipliers.append(3)
    #         else:
    #             letter_multipliers.append(1)

    #         if mult == "DW":
    #             word_multiplier *= 2
    #         elif mult == "TW":
    #             word_multiplier *= 3

    #     return {
    #         "row": row,
    #         "col": col,
    #         "direction": direction,
    #         "letter_multipliers": letter_multipliers,
    #         "word_multiplier": word_multiplier,
    #     }
#...............ensure they are connected and start at centre......
    def place_word(self, word, row, col, direction, dry_run=False):
        word = word.upper()
        letter_multipliers = []
        word_multiplier = 1

        touching_existing_letter = False
        board_has_letters = any(any(cell is not None for cell in row_) for row_ in self.grid)

        for i, ch in enumerate(word):
            r, c = (row, col + i) if direction == "H" else (row + i, col)

            # Check out-of-bounds
            if not (0 <= r < 15 and 0 <= c < 15):
                if dry_run:
                    return None
                else:
                    raise ValueError(f"Out of bounds: {word} at ({r}, {c})")

            current_cell = self.grid[r][c]

            if current_cell is not None:
                if current_cell != ch:
                    # Conflicting letter
                    if dry_run:
                        return None
                    else:
                        raise ValueError(f"Conflicting letter at ({r}, {c})")
                else:
                    touching_existing_letter = True
            else:
                # Check if this cell is adjacent to any filled cell
                for dr, dc in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nr, nc = r + dr, c + dc
                    if 0 <= nr < 15 and 0 <= nc < 15 and self.grid[nr][nc]:
                        touching_existing_letter = True

            # Actually place letter if it's not a dry run
            if current_cell is None and not dry_run:
                self.grid[r][c] = ch

            # Scoring logic
            mult = MULTIPLIER_LAYOUT[r][c]
            if mult == "DL":
                letter_multipliers.append(2)
            elif mult == "TL":
                letter_multipliers.append(3)
            else:
                letter_multipliers.append(1)

            if mult == "DW":
                word_multiplier *= 2
            elif mult == "TW":
                word_multiplier *= 3

        # Validate connection
        if dry_run:
            if not board_has_letters:
                # First word must go through center
                if direction == "H":
                    covers_center = row == 7 and col <= 7 and col + len(word) > 7
                else:
                    covers_center = col == 7 and row <= 7 and row + len(word) > 7
                if not covers_center:
                    return None
            else:
                if not touching_existing_letter:
                    return None

        return {
            "row": row,
            "col": col,
            "direction": direction,
            "letter_multipliers": letter_multipliers,
            "word_multiplier": word_multiplier,
        }


    

    # def display(self):
    #     """Print board with letters or '.' for empty cells"""
    #     for row in self.grid:
    #         print(" ".join(ch if ch else "." for ch in row))

    # def display(self):
    #     """Print board with letters or '.' for empty cells, including row/column indexes."""
    #     size = len(self.grid)
        
    #     # Print column headers
    #     print("    " + " ".join(f"{i:2}" for i in range(size)))
        
    #     for idx, row in enumerate(self.grid):
    #         # Print row index and row contents
    #         print(f"{idx:2}  " + " ".join(ch if ch else "." for ch in row))

    def display(self):
        """Print board with letters or '.' for empty cells, including row/column indexes, aligned."""
        size = len(self.grid)
        
        # Print column headers with fixed width 3 per column (2 digits + space)
        print("    " + " ".join(f"{i:2}" for i in range(size)))
        
        for idx, row in enumerate(self.grid):
            # Print row index (2 spaces), then the row cells each padded to 2 spaces
            row_str = " ".join(f"{ch if ch else '.':2}" for ch in row)
            print(f"{idx:2}  {row_str}")


