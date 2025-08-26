import time
from functools import wraps
from models.player import Player

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
        Player.username= getattr(args[0], "Player.username", "Unknown") if args else "Unknown"
        txt = f"Player: {Player.username}, Function: {func.__name__}, Time taken: {diff} sec"
        write_file("game_log.txt", txt)
        return result
    return wrapper
