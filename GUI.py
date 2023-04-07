import time
from tkinter import *
from tkinter.ttk import *
from tkinter.filedialog import askopenfile
import grammar
import tokens_scanner as tk_sc

screen = Tk()
screen.title("Compiler project")
screen.geometry("700x500")
filename = "File not uploded yet"


def read_file():
    file_path = askopenfile(mode="r", filetypes=(("Text Files", "*.txt"),))
    global filename
    filename = str(file_path.name)
    if file_path is not None:
        uploded_filename = Label(screen, text=filename)
        uploded_filename.grid(row=10, column=1)
        with open(file_path.name, "r") as r:
            code_lines = r.readlines()
            token_scanner_outputs = tk_sc.scanner(code_lines)
            grammar.outputs = token_scanner_outputs
            grammar.program()
            grammar.generate_tree()
            print("hello", token_scanner_outputs)

        


def create_GUI():
    action_button_label = Label(screen, text="Upload tiny code code")
    action_button_label.grid(row=0, column=0, padx=10)

    action_button = Button(screen, text="Choose tiny code file", command=lambda: read_file())
    action_button.grid(row=0, column=1)

    uploded_filename_label = Label(screen, text="Uploded filename :")
    uploded_filename_label.grid(
        row=10,
        column=0,
    )


    screen.mainloop()


