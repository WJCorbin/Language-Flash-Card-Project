import tkinter as gui
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
LEARNING_LANGUAGE = "French"
NATIVE_LANGUAGE = "English"
global timer
global new_word


# Flip card
# Button Click
def next_card():
    global timer, new_word
    new_word = random.choice(word_list)
    canvas.itemconfig(card, image=card_front_img)
    canvas.itemconfig(language, text=LEARNING_LANGUAGE, fill="black")
    canvas.itemconfig(word, text=new_word[LEARNING_LANGUAGE], fill="black")
    timer = window.after(5000, flip_card)


def flip_card():
    global new_word
    window.after_cancel(timer)
    canvas.itemconfig(card, image=card_back_img)
    canvas.itemconfig(language, text=NATIVE_LANGUAGE, fill="white")
    canvas.itemconfig(word, text=new_word[NATIVE_LANGUAGE], fill="white")
    new_word = random.choice(word_list)


# If card was known
def known():
    word_list.remove(new_word)
    next_card()
    data_frame = pandas.DataFrame(word_list)
    data_frame.to_csv("data/need_to_learn.csv", index=False)


# GUI
window = gui.Tk()
window.title("Language Learning Flash Cards")
window.config(bg=BACKGROUND_COLOR, padx=50, pady=50)
card_front_img = gui.PhotoImage(file="images/card_front.png")
card_back_img = gui.PhotoImage(file="images/card_back.png")
yes_img = gui.PhotoImage(file="images/right.png")
no_img = gui.PhotoImage(file="images/wrong.png")
canvas = gui.Canvas(width=800, height=526, bg=BACKGROUND_COLOR, highlightthickness=0)
card = canvas.create_image(400, 263, image=card_front_img)
language = canvas.create_text(400, 150, font=("Ariel", 40, "italic"))
word = canvas.create_text(400, 263, font=("Ariel", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)
yes_button = gui.Button(image=yes_img, highlightthickness=0, borderwidth=0, command=known)
yes_button.grid(column=1, row=1)
no_button = gui.Button(image=no_img, highlightthickness=0, borderwidth=0, command=next_card)
no_button.grid(column=0, row=1)

# Program
try:
    data = pandas.read_csv("data/need_to_lean.csv")
except FileNotFoundError:
    data = pandas.read_csv("data/french_words.csv")

word_list = data.to_dict(orient="records")

next_card()

window.mainloop()
