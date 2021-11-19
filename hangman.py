## Author: Anne De Vreyer
## Date: October 2021
## This program is GUI game of hangman.
## The player is prompted for a letter via dialogbox.
## A new stage of the hangman is drawn when they guess wrong.
## If they guess right, the correct letter is added to the display of dashes and letters.
## Word possibilities are loaded from a pickled list.
## Input file is pickled list of string, each item in the list is a word.
## Input file name: countries_hangman.dat


# Import modules for GUI etc.
import turtle
from tkinter import messagebox
import pickle
import random


class RandomWord:
    def __init__(self, input_file):
        # Load word list from input file.
        self.__input_file = open(input_file, "rb")
        self.__word_list = pickle.load(self.__input_file)
        self.__input_file.close()
        # Initialize letter list.
        self.__letter_list = []
        # Pick a random word for hangman game.
        self.__word = random.choice(self.__word_list).upper()
        # Dashes at beginning of game, based on length of selected word.
        self.__first_dashes = self.create_first_dashes()

    # Print method will print generated word.
    def __str__(self):
        return self.__word

    # Accessor methods
    def get_word(self):
        return self.__word.upper()

    def get_first_dashes(self):
        return self.__first_dashes

    # Dashes based on length of randomly selected word.
    def create_first_dashes(self):
        dashes = ""
        for char in self.__word:
            if char != " ":
                dashes += "_ "
            else:
                dashes += "  "
        return dashes

    # Makes a first list of dashes from word to guess.
    def make_list(self):
        for char in self.__word:
            if char != " ":
                self.__letter_list.append("_ ")
            else:
                self.__letter_list.append(" ")
        return self.__letter_list

    # Makes a word from list of letters correctly guessed.
    def make_word(self):
        word_guessed = ""
        for char in self.__letter_list:
            word_guessed += char
        return word_guessed

    # Creates new list if guessed letter is correct.
    def make_correct_list(self):
        index_list = [index for index in range(len(self.__word)) if self.__word.find(self.__letter, index) == index]
        for index in index_list:
            self.__letter_list[index] = self.__letter  # Updated list used to build word for display in Turtle.

    # Gets player's letter, does input validation, returns letter.
    def ask_letter(self):
        while True:
            try:
                self.__letter = turtle.textinput("Guess", "Enter a letter: ")
                self.__letter = self.__letter.upper()
                # Input validation.
                while len(self.__letter) != 1 or not self.__letter.isalpha():
                    messagebox.showerror(title="Not a letter", message="Woops, that's not a single letter! Try again")
                    self.__letter = turtle.textinput("Guess", "Enter a letter: ")
                    self.__letter = self.__letter.upper()
                return self.__letter
                break
            except AttributeError:  # If player clicks "cancel/close" in textinput box
                choice = messagebox.askyesno(title="Cancelled",
                                             message="Would you like to quit the game?")
                if choice:
                    quit()
                else:
                    continue


# Game interface. Attributes dashes depends on word to guess.
class Hangman:
    def __init__(self, dashes, word):
        self.__dashes = dashes
        self.__length = 35 * len(word)
        self.__counter = 0  # Counter initializes as zero with new game.
        self.__lost = False  # Flag, when True player has lost.
        # Basic settings of canvas.
        turtle.bgcolor("light yellow")
        turtle.setup(width=0.75, height=0.75)
        turtle.hideturtle()
        turtle.speed(8)
        # Word to guess area.
        self.draw_rectangle()  # White background.
        self.draw_underscore()  # Dashes.

    # Mutator method.
    def set_dashes(self, dashes):
        self.__dashes = dashes

    # Accessor methods.
    def get_counter(self):
        return self.__counter

    def get_lost(self):
        return self.__lost

    # Counter increased by 1 when player guesses wrong.
    def update_counter(self):
        self.__counter += 1

    # Draws background white rectangle for word.
    def draw_rectangle(self):
        turtle.speed(0)
        turtle.penup()
        turtle.goto(180, 260)
        # Draw background white rectangle for word.
        turtle.pendown()
        turtle.fillcolor("white")
        turtle.pencolor("white")
        turtle.begin_fill()
        # Rectangle. Avoid use of setheading() or weird shapes happen.
        turtle.goto(180 + self.__length, 260)
        turtle.goto(180 + self.__length, 360)
        turtle.goto(180, 360)
        turtle.goto(180, 260)
        turtle.end_fill()

    # Writes word with dashes and correct letters.
    def draw_underscore(self):
        font_style = ("Calibri", 30, "bold")
        turtle.speed(0)
        turtle.penup()
        turtle.pencolor("black")
        x_start = 180 + self.__length / 2  # Starting point for word depends on its length.
        turtle.goto(x_start, 280)
        turtle.pendown()
        turtle.write(self.__dashes, align="CENTER", font=font_style)
        turtle.speed(8)
        turtle.penup()

    # Draw each stage of hangman depending on counter value.
    def draw(self):
        if self.__counter == 1:
            # Stand
            turtle.pensize(20)
            turtle.pencolor("brown")
            turtle.penup()
            # 1 Bottom of stand
            turtle.goto(260, -300)  # Starting point
            turtle.pendown()
            turtle.goto(-260, -300)
            turtle.penup()

        if self.__counter == 2:
            # 2 Side of stand
            turtle.pensize(20)
            turtle.pencolor("brown")
            turtle.penup()
            turtle.goto(-260, -300)
            turtle.pendown()
            turtle.goto(-260, 300)
            turtle.penup()

        if self.__counter == 3:
            # 3 Top of stand
            turtle.pensize(20)
            turtle.pencolor("brown")
            turtle.penup()
            turtle.goto(-260, 300)
            turtle.pendown()
            turtle.goto(0, 300)
            turtle.penup()

        if self.__counter == 4:
            # 4 Little corner thing
            turtle.penup()
            turtle.pencolor("brown")
            turtle.goto(-200, 300)
            turtle.pendown()
            turtle.goto(-260, 260)
            turtle.penup()

        if self.__counter == 5:
            # 5 Noose
            turtle.penup()
            turtle.pencolor("gold")
            turtle.pensize(15)
            turtle.goto(0, 300)
            turtle.pendown()
            turtle.setheading(270)
            turtle.forward(60)
            turtle.penup()

        if self.__counter == 6:
            # 6 Head
            turtle.penup()
            turtle.pencolor("black")
            turtle.setheading(270)
            turtle.pensize(5)
            turtle.goto(-30, 210)
            turtle.pendown()
            turtle.fillcolor("white")
            turtle.begin_fill()
            turtle.circle(30)
            turtle.end_fill()
            turtle.penup()

        if self.__counter == 7:
            # 7 Body
            turtle.penup()
            turtle.goto(0, 180)
            turtle.pendown()
            turtle.goto(0, 0)
            turtle.penup()

        if self.__counter == 8:
            # 8 Left arm
            turtle.penup()
            turtle.goto(0, 170)
            turtle.pendown()
            turtle.setheading(310)
            turtle.forward(90)
            turtle.penup()

        if self.__counter == 9:
            # 9 Right arm
            turtle.penup()
            turtle.goto(0, 170)
            turtle.pendown()
            turtle.setheading(230)
            turtle.forward(90)
            turtle.penup()

        if self.__counter == 10:
            # 10 Left leg
            turtle.penup()
            turtle.goto(0, 0)
            turtle.pendown()
            turtle.setheading(290)
            turtle.forward(150)
            turtle.penup()

        if self.__counter == 11:
            # 11 Right leg
            turtle.penup()
            turtle.goto(0, 0)
            turtle.pendown()
            turtle.setheading(250)
            turtle.forward(150)
            turtle.penup()
            self.__lost = True


def main():
    # Initialize variables.
    guessed_word = ""  # Word built on base of successful letter guesses.

    # Create a Word object and get relevant attributes.
    Word1 = RandomWord("countries_hangman.dat")
    word = Word1.get_word()
    dashes = Word1.get_first_dashes()

    # Create hangman and set variables.
    Hangman1 = Hangman(dashes, word)
    lost = Hangman1.get_lost()

    # Get list of letters from word.
    Word1.make_list()

    # Game goes on until player reaches max number of wrong guesses or guesses the word.
    while not lost and guessed_word != word:
        letter = Word1.ask_letter()

        if letter in word:
            Word1.make_correct_list()
            guessed_word = Word1.make_word()
            Hangman1.set_dashes(guessed_word)
            Hangman1.draw_rectangle()
            Hangman1.draw_underscore()

        else:
            Hangman1.update_counter()  # Counter dictates step of drawing and if lost.
            Hangman1.draw()
            lost = Hangman1.get_lost()

    if guessed_word == word:
        messagebox.showinfo(title="Well done!", message="You won!")

    elif lost:
        messagebox.showinfo(title="Oh no!", message=f"You lost! The word was: {word}.")

if __name__ == '__main__':
    main()
    turtle.done()

