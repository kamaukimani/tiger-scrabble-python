import time
from functools import wraps

def write_file(f_name, txt):
    with open(f_name, 'a') as file:
        file.write(f"{txt}\n")

def logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        diff = round(end_time - start_time, 2)

        # Safely extract player username if available
        player_name = "Unknown"
        if args and hasattr(args[0], "player") and hasattr(args[0].player, "username"):
            player_name = args[0].player.username

        txt = f"Player: {player_name}, Function: {func.__name__}, Time taken: {diff} sec"
        write_file("game_log.txt", txt)
        return result
    return wrapper
