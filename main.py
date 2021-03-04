from tkinter import *
from tkinter import messagebox
import pandas
import random

BACKGROUND_COLOR = "#B1DDC6"
DATA_FILE = "data/rench_words.csv"
WORDS_TO_LEARN = "data/ord_to_learn.csv"
DELAY = 5000
current_word = {}


def read_words_data():
    df = None
    try:
        df = pandas.read_csv(WORDS_TO_LEARN).to_dict(orient="records")
        print("words to learn file found")
    except FileNotFoundError:
        try:
            df = pandas.read_csv(DATA_FILE).to_dict(orient="records")
            print("there was no words to learn file, french words file initialized")
        except FileNotFoundError:
            print("No Data file")
    finally:
        return df


def word_learnt():
    data.remove(current_word)
    save_words_to_learn()
    generate_word()


def save_words_to_learn():
    df = pandas.DataFrame(data)
    df.to_csv(WORDS_TO_LEARN, index=False)


# ---------------------------- Card Functions ------------------------------- #

def generate_word():
    try:
        word = random.choice(data)
    except TypeError:
        messagebox.showwarning(title="Input Data Error", message="Data Initialized With errors")
    else:
        canvas.itemconfig(title_text, text="French", fill="black")
        canvas.itemconfig(word_text, text=word['French'], fill="black")
        canvas.itemconfig(card_image, image=card_front)
        root.after(DELAY, flip_card)

        global current_word
        current_word = word


def flip_card():
    canvas.itemconfig(title_text, text="English", fill="white")
    canvas.itemconfig(word_text, text=current_word['English'], fill="white")
    canvas.itemconfig(card_image, image=card_back)
    root.after_cancel(flip_card)


# ---------------------------- Initialization ------------------------------- #

# data = pandas.read_csv(DATA_FILE).to_dict(orient="records")
data = read_words_data()

# ---------------------------- UI SETUP ------------------------------- #
root = Tk()
root.title("Flashy")
root.config(padx=50, pady=50, bg=BACKGROUND_COLOR)

# Card
canvas = Canvas(width=800, height=526, highlightthickness=0, bg=BACKGROUND_COLOR)
card_front = PhotoImage(file="images/card_front.png")
card_back = PhotoImage(file="images/card_back.png")
card_image = canvas.create_image(400, 263, image=card_front)
title_text = canvas.create_text(400, 150, text="French", fill="black", font=("Arial", 40, "italic"))
word_text = canvas.create_text(400, 263, text=f"",
                               fill="black", font=("Arial", 60, "bold"))
canvas.grid(column=0, row=0, columnspan=2)

# Wrong Button
wrong_icon = PhotoImage(file="images/wrong.png")
wrong_button = Button(image=wrong_icon, highlightthickness=0,
                      activebackground=BACKGROUND_COLOR, bd=0, command=generate_word)
wrong_button.grid(column=0, row=1)

# Right Button
right_icon = PhotoImage(file="images/right.png")
right_button = Button(image=right_icon, highlightthickness=0,
                      activebackground=BACKGROUND_COLOR, bd=0, command=word_learnt)
right_button.grid(column=1, row=1)

generate_word()

root.mainloop()
