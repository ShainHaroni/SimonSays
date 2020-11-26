import tkinter as tk
import random
from tkinter import messagebox
import pygame

class SimonSays:
    def __init__(self, parent):
        self.parent = parent
        self.draw_board()
        self.canvas = tk.Canvas(self.parent, height=600, width=600)
        self.canvas.pack()
        self.dark = {'r': 'darkred', 'g': 'darkgreen', 'b': 'darkblue', 'y': 'darkgoldenrod'}
        self.light = {'r': 'red', 'g': 'green', 'b': 'blue', 'y': 'lightgoldenrod'}
        self.squares = {'r': self.canvas.create_rectangle(0, 0, 300, 300, fill='darkred', outline='darkred'),
                        'g': self.canvas.create_rectangle(300, 0, 600, 300, fill='darkgreen', outline='darkgreen'),
                        'b': self.canvas.create_rectangle(0, 300, 300, 600, fill='darkblue', outline='darkblue'),
                        'y': self.canvas.create_rectangle(300, 300, 600, 600, fill='darkgoldenrod',
                                                          outline='darkgoldenrod')}

        self.status = tk.Label(root, text="Let's play Simon Says")
        self.high_score = 0
        self.selections = ""
        self.status.pack()
        self.parent.bind('<h>', self.score)
        self.ids = {v: k for k, v in self.squares.items()}
        self.draw_board()

    def draw_board(self):
        self.pattern = random.choice('rgby')
        self.selections = ''
        self.parent.after(800, self.animate)

    def animate(self, index=0):
        color_chosen = self.pattern[index]
        self.canvas.itemconfig(self.squares[color_chosen], fill=self.light[color_chosen], outline=self.light[color_chosen])
        self.music()
        self.parent.after(500, lambda: self.canvas.itemconfig(self.squares[color_chosen], fill=self.dark[color_chosen], outline=self.dark[color_chosen]))
        index += 1
        if index < len(self.pattern):
            self.parent.after(800, lambda: self.animate(index))
        else:
            self.canvas.bind('<1>', self.select)
            print(self.pattern)

    def music(self):

        if self.pattern == 'r':
            pygame.mixer.music.load("beep1.ogg")
        elif self.pattern == 'g':
            pygame.mixer.music.load("beep2.ogg")
        elif self.pattern == 'b':
            pygame.mixer.music.load("beep3.ogg")
        elif self.pattern == 'y':
            pygame.mixer.music.load("beep4.ogg")
        pygame.mixer.music.play()

    def select(self, event = None):
        id = self.canvas.find_withtag("current")[0]
        color = self.ids[id]
        self.selections += self.ids[id]
        self.canvas.itemconfig(id, fill=self.light[color], outline=self.light[color])
        self.parent.after(200, lambda: self.canvas.itemconfig(id, fill=self.dark[color], outline=self.dark[color]))
        if self.pattern[len(self.selections) - 1] != color:
            self.canvas.unbind('<1>')
            self.parent.after(2000, self.draw_board)
            self.play_again()
        elif self.pattern == self.selections:
            self.canvas.unbind('<1>')
            self.status.config(text="Correct!")
            self.parent.after(3000, lambda: self.status.config(text=""))
            self.pattern += random.choice('rgby')
            self.selections = ''
            self.high_score = max(self.high_score, len(self.pattern))
            self.parent.after(500, self.animate)

    def score(self, event=None):
        self.parent.after(1000, lambda: self.status.config(text=""))

    def play_again(self):
        response = messagebox.askquestion("Game Over",
                                  f"You lost the game with {self.high_score} points \n Do you want play Simon Says again?")
        if response == "yes":
            pass
        elif response == "no":
            self.quit()

    def quit(self):
        root.quit()

root = tk.Tk()
root.configure(background="light grey")
root.title("Simon Says App")
pygame.mixer.init()
simon = SimonSays(root)
root.mainloop()