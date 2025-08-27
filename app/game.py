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
        self.played_words = set()  # track all played words 

        self.human_score = 0
        self.computer_score = 0

        self.player_rack = []    
        self.computer_rack = []

        self.turn_counter = 0  # To track number of turns
        self.max_turns = 4     # Max turns before ending the game

        self.setup_player()

    def get_valid_string(self, prompt):
        while True:
            value = input(prompt).strip()
            if not value:
                print("Input cannot be empty. Try again.")
                continue
            if not value.replace(" ", "").isalpha():  # allows names like "John Doe"
                print("Only alphabetic characters are allowed. Try again!")
                continue
            return value.title()

    def get_valid_password(self, prompt):
        while True:
            password = input(prompt).strip()
            if not password.isdigit():
                print("Password must contain only digits (0-9). Try again!")
                continue
            if len(password) < 4:
                print("Password must be at least 4 digits long. Try again!")
                continue
            return password

    def setup_player(self):
        username = self.get_valid_string("Enter your username: ")
        player = self.session.query(Player).filter(Player.username == username).first()

        if not player:
            country = self.get_valid_string("Enter your country: ")
            password = self.get_valid_password("Set your password (numbers only, min 4 digits): ")
            player = Player(username=username, country=country, password=password)
            self.session.add(player)
            self.session.commit()
            self.session.refresh(player)
        else:
            # Existing player: check password
            attempts = 3
            while attempts > 0:
                password = input(f"Enter your password ({attempts} attempts remaining): ")
                if player.password == password:
                    print("Login successful.")
                    break
                else:
                    attempts -= 1
                    print("Incorrect password.")
            else:
                print("Too many failed attempts. CONTACT PAUL......Exiting game.....")
                exit(1)

        self.player = player

        # Load or create game
        game = self.session.query(Game).filter(Game.player_id == player.id).first()
        if not game:
            game = Game(player_id=player.id, board=self.board.grid)
            self.session.add(game)
            self.session.commit()
            self.session.refresh(game)
        else:
            # Load saved board
            self.board.grid = game.board

        self.game_record = game
        self.played_words = set(game.played_words or [])
        self.human_score = game.human_score or 0
        self.computer_score = game.computer_score or 0

        # Load or draw player rack
        if game.player1_rack:
            self.player_rack = game.player1_rack
        else:
            self.player_rack = self.draw_tiles(7)
            game.player1_rack = self.player_rack
        
        # Ask if human vs Computer
        choice = input("Play against Computer ? (y/n): ").lower()
        if choice == "y":
            self.computer_player = Computer(self)
            if game.player2_rack:
                self.computer_rack = game.player2_rack
            else:
                self.computer_rack = self.draw_tiles(7)
                game.player2_rack = self.computer_rack

    @logger
    def draw_tiles(self, n):
        return self.tile_bag.draw(n)

    @logger
    def play_turn(self, player_rack=None, is_computer=False):
        #Main logic for one turn (human or computer)
        self.board.display()

        if is_computer and self.computer_player:
            # Check if the computer can make a valid move
            if not self.can_form_any_valid_word(self.computer_rack):
                print("Computer cannot make a move. The game is over.")
                self.end_game()  # End the game if the computer can't make a move
                return

            word, placement, score = self.computer_player.play(self.computer_rack)
            if word:
                self.computer_score += score
                self.played_words.add(word)
                print(f"Computer scored: {score} | Total: {self.computer_score}")
                # Refill computer rack
                tiles_needed = 7 - len(self.computer_rack)
                self.computer_rack.extend(self.draw_tiles(tiles_needed))
            return

        # Human turn
        while True:
            # Show the player's current rack
            print(f"Your current rack contains the following letters: {', '.join(player_rack)}")

            # Check if any valid word can be formed with the current rack
            if not self.can_form_any_valid_word(player_rack):
                reset_choice = input("No valid word can be formed with your current rack. Would you like to reset it? (y/n): ").strip().lower()
                if reset_choice == "y":
                    self.reset_rack(player_rack)
                    print("Your rack has been reset with new tiles.")
                    continue
                else:
                    print("You chose not to reset the rack. Try entering a valid word.")
                    continue
            word = input("Enter word to play (or type 'quit'  exit or 'reset' to reset your rack): ").strip()

            if word.lower() in ("quit", "exit"):
                print("Exiting game...")
                self.save_game()
                print("You have successfully exited. See you next time!")
                exit(0)

            if word.lower() == "reset":
                reset_confirmation = input("Are you sure you want to reset your rack? (y/n): ").strip().lower()
                if reset_confirmation == 'y':
                    print("Your rack has been reset.")
                    self.reset_rack(player_rack)  # Reset the rack
                    break  # Exit the turn loop to allow the player to draw new tiles
                else:
                    print("Rack reset canceled. Continuing with your turn.")
                    continue

            if not word:
                print("No word entered. Try again.")
                continue

            word = word.upper()

            # Check if the word can be formed from player's rack
            if not self.can_form_word_from_rack(word, player_rack):
                print(f"You don't have the necessary tiles to form '{word}'. Try another word.")
                continue
            # Check if word was already played
            if word in self.played_words:
                print(f"The word '{word}' has already been played. Try another word.")
                continue
            if not self.dictionary.is_valid(word):
                print("Invalid word. Try again.")
                continue

            try:
                row = int(input("Row (0-14): "))
                col = int(input("Col (0-14): "))
            except ValueError:
                print("Invalid row/column input. Please enter numbers.")
                continue

            direction = input("Direction (H/V): ").strip().upper()
            if direction not in ("H", "V"):
                print("Invalid direction. Please enter 'H' or 'V'.")
                continue

            placement = self.board.place_word(word, row, col, direction, dry_run=True)
            if not placement:
                print("Invalid word placement. Try again.")
                continue

            score = score_word(word, placement)
            confirm = input(f"Play '{word}' at ({row},{col}) {direction}? Score: {score} (y/n): ").lower()
            if confirm == "y":
                self.board.place_word(word, row, col, direction)  # Final placement
                self.played_words.add(word) 
                self.human_score += score
                print(f"You scored: {score} | Total: {self.human_score}")

                # Remove letters from player's rack
                self.remove_letters_from_rack(word, player_rack)
                # Refill human player's rack
                tiles_needed = 7 - len(self.player_rack)
                self.player_rack.extend(self.draw_tiles(tiles_needed))

                break

    def save_game(self):
         #Save current board and updated time
        self.game_record.board = copy.deepcopy(self.board.grid)
        self.game_record.played_words = list(self.played_words)
        self.game_record.player1_rack = self.player_rack
        self.game_record.player2_rack = self.computer_rack if self.computer_player else None
        self.game_record.human_score = self.human_score
        self.game_record.computer_score = self.computer_score
        self.session.commit()
        self.session.refresh(self.game_record)

    def start_game(self):
        #Main game loop with turn tracking and database refresh
        while True:
            self.session.refresh(self.game_record)

            print(f"\n[TURN] {'Human' if self.game_record.is_player_turn else 'Computer'}'s turn.")
            print(f"Scores for Human: {self.human_score} | Computer: {self.computer_score}")

            if self.computer_player:
                if self.game_record.is_player_turn:
                    self.play_turn(player_rack=self.player_rack)
                    self.game_record.is_player_turn = False
                else:
                    self.play_turn(player_rack=self.computer_rack, is_computer=True)
                    self.game_record.is_player_turn = True
            else:
                self.play_turn(player_rack=self.player_rack)

            self.turn_counter += 1
            self.save_game()

            proceed = input("Continue game? (y/n): ").lower()
            if proceed != "y":
                print("Game saved. Goodbye!")
                break

            # End game after 4 turns
            if self.turn_counter >= self.max_turns:
                self.end_game()
                break

    def end_game(self):
        #End the game, announce the winner and loser, and capture the winner's name without saving it to the database.
        print("\nGame Over!")

        # Determine the winner and loser, then print messages accordingly
        if self.human_score > self.computer_score:
            winner = self.player.username  # Human player wins
            loser = "Computer"  # Computer loses
            print(f"Congratulations, {winner}! You win! Final score: {self.human_score} - {self.computer_score}")
            print(f"Computer loses! Final score: {self.computer_score} - {self.human_score}")
        elif self.human_score < self.computer_score:
            winner = "Computer"  # Computer wins
            loser = self.player.username  # Human player loses
            print(f"Computer wins! Final score: {self.computer_score} - {self.human_score}")
            print(f"{self.player.username} loses! Final score: {self.human_score} - {self.computer_score}")
        else:
            winner = "None"  # It's a draw
            loser = "None"  # No loser in case of a draw
            print(f"It's a draw! Final score: {self.human_score} - {self.computer_score}")

        print("Game over. Thank you for playing!")
        return winner, loser



    def can_form_any_valid_word(self, rack):
        #Check if any valid word can be formed from the player's rack.
        for word in self.dictionary.get_all_valid_words():
            if self.can_form_word_from_rack(word, rack):
                return True
        return False

    def can_form_word_from_rack(self, word, rack):
        #Check if a given word can be formed from the player's rack.
        rack_copy = list(rack)
        for letter in word:
            if letter in rack_copy:
                rack_copy.remove(letter)
            else:
                return False
        return True

    def remove_letters_from_rack(self, word, rack):
        #Remove the letters used in the word from the player's rack.
        for letter in word:
            rack.remove(letter)

    def reset_rack(self, player_rack):
        #Reset the player's rack by drawing new tiles from the tile bag.
        player_rack.clear()  # Clear the current rack
        new_tiles = self.draw_tiles(7)  # Draw 7 new tiles from the tile bag
        player_rack.extend(new_tiles)  # Add the new tiles to the rack
        print(f"New rack: {', '.join(player_rack)}")  # Show the new rack to the player
