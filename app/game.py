from app.db import SessionLocal
from models.player import Player
from models.game import Game
from .tiles import TileBag
from .board import Board
from .scoring import score_word
from .dictionary import Dictionary
from .computer import Computer
from .logger import logger
import random
import copy

class ScrabbleGame:
    def __init__(self):
        self.session = SessionLocal()
        self.dictionary = Dictionary()
        self.tile_bag = TileBag()
        self.board = Board()
        self.player = None
        self.game_record = None
        self.computer_player = None

        self.setup_player()

    def setup_player(self):
        username = input("Enter your username: ")
        player = self.session.query(Player).filter(Player.username==username).first()

        if not player:
            country = input("Enter your country: ")
            player = Player(username=username, country=country)
            self.session.add(player)
            self.session.commit()
            self.session.refresh(player)

        self.player = player

        # Load or create game
        game = self.session.query(Game).filter(Game.player_id==player.id).first()
        if not game:
            game = Game(player_id=player.id, board=self.board.grid)
            self.session.add(game)
            self.session.commit()
            self.session.refresh(game)
        else:
            # Load saved board
            self.board.grid = game.board

        self.game_record = game

        # Ask if human vs Computer
        choice = input("Play against Computer ? (y/n): ").lower()
        if choice == "y":
            self.computer_player = Computer (self)

    @logger
    def draw_tiles(self, n):
        return self.tile_bag.draw(n)

    @logger
    def play_turn(self, player_rack):
        """
        Main logic for one turn (human input or Computer )
        """
        self.board.display()
        if self.computer_player and player_rack == "Computer ":
            # Computer  turn
            word, placement, score = self.computer_player.play(player_rack)
            print(f"Computer  scored: {score}")
            return

        # Human turn

#-----------------add quit anytime------
        # while True:
        #     word = input("Enter word to play: ").upper()
        #     if not self.dictionary.is_valid(word):
        #         print("Invalid word. Try again.")
        #         continue
#-----------------add quit anytime------
        while True:
            word = input("Enter word to play (or type 'quit' to exit): ").strip()
            
            if word.lower() in ("quit", "exit"):
                print("Exiting game...")
                self.save_game()
                exit(0)  # or: return, depending on how you want to exit

            if not word:
                print("No word entered. Try again or type 'quit' to exit.")
                continue

            word = word.upper()
            if not self.dictionary.is_valid(word):
                print("Invalid word. Try again.")
                continue


            row = int(input("Row (0-14): "))
            col = int(input("Col (0-14): "))
            direction = input("Direction (H/V): ").upper()
            # placement = self.board.place_word(word, row, col, direction, dry_run=True)
            # score = score_word(word, placement)
            # confirm = input(f"Play '{word}' at ({row},{col}) {direction}? Score: {score} (y/n): ").lower()
            # if confirm == "y":
            #     # Place for real
            #     self.board.place_word(word, row, col, direction)
            #     break
            placement = self.board.place_word(word, row, col, direction, dry_run=True)

            if not placement:
                print("Invalid word placement. Try again.")
                continue  # Ask for a new word/position

            score = score_word(word, placement)
            confirm = input(f"Play '{word}' at ({row},{col}) {direction}? Score: {score} (y/n): ").lower()
            if confirm == "y":
                self.board.place_word(word, row, col, direction)  # Place for real
                break


        print(f"You scored: {score}")

    def save_game(self):
        """
        Save current board and updated time
        """
        self.game_record.board = copy.deepcopy(self.board.grid)
        self.session.commit()
        self.session.refresh(self.game_record)

    def start_game(self):
        """
        Main game loop
        """
        while True:
            if self.computer_player:
                # Human turn
                self.play_turn(player_rack=self.draw_tiles(7))
                self.save_game()

                # Computer  turn
                self.play_turn(player_rack="Computer ")
                self.save_game()
            else:
                # Human vs Human
                self.play_turn(player_rack=self.draw_tiles(7))
                self.save_game()

            cont = input("Continue game? (y/n): ").lower()
            if cont != "y":
                print("Game saved. Goodbye!")
                break
