from .tiles import LETTER_POINTS

def score_word(word, placement):
    word = word.upper()
    letter_multipliers = placement.get("letter_multipliers", [1] * len(word))
    word_multiplier = placement.get("word_multiplier", 1)

    total = 0
    for i, ch in enumerate(word):
        base = LETTER_POINTS.get(ch, 0)
        lm = letter_multipliers[i] if i < len(letter_multipliers) else 1
        total += base * lm

    return total * word_multiplier
