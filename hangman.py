import argparse
import random
import re

class Hangman:
	def __init__(self, max_guesses: int, dictionary: str = "en_words.txt", retain_correct_guess: bool = False):
		self.load_dictionary("assets/" + dictionary)
		self.remaning_guesses = max_guesses
		self.retain_correct_guess = retain_correct_guess

	def run(self):
		self.start_game()

		print(f"A random letter has been chosen from among {len(self.dictionary)} words!")
		print(f"The word has {len(self.word)} letters in it")

		while True:
			# check for any remaning guesses
			if self.remaning_guesses <= 0:
				self.end_game(False)
				break

			# check if all chars in the word has been guessed
			if self.all_chars_in_word_guessed():
				self.end_game(True)
				break

			# make a guess
			self.print_game_state()
			current_guess = input("Guess the word: ");
			if not self.guess(current_guess) or self.retain_correct_guess:
				self.guess_count += 1
				self.remaning_guesses -= 1

            # check if guess is correct
			if current_guess == self.word:
				self.end_game(True)
				break

	def start_game(self):
		self.word = self.select_random_word_from_dictionary()
		self.guess_count = 0
		self.guesses = []

	def end_game(self, success: bool):
		print() # newline

		if success:
			print("You guessed the word! Congratulations!")
		else:
			print("You unfortunately failed... better luck next time")

		print("Game statistics:")
		print(f"- word: {self.word}")
		print(f"- guesses: {self.guess_count}")
		print(f"- remaining guesses: {self.remaning_guesses}")

	def guess(self, guess: str) -> bool:
		if len(guess) > 1:
			# is guessing the word
			if guess == self.word:
				return True
			else:
				print(f"{guess} is not the word!")
		else:
			# is guessing a character
			self.guesses.append(guess)

			if guess in self.word:
				print(f"The letter {guess} is in the word")
				return True
			else:
				print(f"The letter {guess} is not in the word")

		return False

	def print_game_state(self):
		print(f"Remaining guesses: {self.remaning_guesses}")
		for letter in self.word:
			if letter in self.guesses:
				print(f" {letter} ", end = "")
			else:
				print(" _ ", end = "")
		print() # newline

	def all_chars_in_word_guessed(self) -> bool:
		for letter in self.word:
			if not letter in self.guesses:
				return False
		return True

	def load_dictionary(self, path: str):
		with open(path) as dictionary_file:
			self.dictionary = dictionary_file.readlines()

	def select_random_word_from_dictionary(self) -> str:
		# select random word from dictionary
		word = random.choice(self.dictionary)

		# filter out abnormal chars
		word = re.sub(r'\W+', '', word)

		return word

# todo
# - rule: dont allow guessing same letter multible times
# - fix bug where the letters æøå get corrupted in the program

if __name__ == "__main__":
	# create command line argument parser
	parser = argparse.ArgumentParser(description = "A simple hangman game")
	parser.add_argument("--dictionary", type=str, default="en_words.txt",
		help="what dictionary to use for the word selection")
	parser.add_argument("--guesses", type=int, default=20,
		help="what dictionary to use for the word selection")
	parser.add_argument("--retain-correct-guess", type=bool, default=False,
		help="do not loose a guess if the guess you made was correct.")
	args = parser.parse_args()

	# run game
	game = Hangman(dictionary = args.dictionary, max_guesses = args.guesses,
			retain_correct_guess = args.retain_correct_guess)
	game.run()

	# halt before exit
	input("Press enter to exit...")
