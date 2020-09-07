from tkinter import Tk, Label, Entry, Button, END
from threading import Thread
from time import sleep


class RootWindow:

    def __init__(self, func):
        self.root_window = Tk()
        self.root_window.title("TAXtoPEC - CherryNpl")
        self.root_window.geometry("380x150")

        self.searching_label = Label(self.root_window,
                                     text="Searching...",
                                     font=("arial", 12))

        if func == 'MISSING_KEY':
            self.root_window.geometry("450x150")
            Label(self.root_window,
                  text="Environment variables in the .env file are missing or wrong",
                  fg="red", font=("arial", 12)).grid(row=1)
            self.root_window.mainloop()
        else:
            self.insert_label = Label(self.root_window,
                                      text="Insert the TAX code of the company: ",
                                      font=("arial", 12))
            self.error_label = Label(self.root_window,
                                     text="You should enter a valid TAX Code", fg="red",
                                     font=("arial", 12))
            self.found = False

            self.tax_input = Entry(self.root_window)
            self.tax_input.bind('<Return>', lambda x: self.thread_runner(func))

            self.next_button = Button(self.root_window,
                                      text="Start",
                                      command=self.search)
            self.submit_button = Button(self.root_window,
                                        text="Search",
                                        command=lambda: self.thread_runner(func))
            self.start()

    def start(self):
        Label(self.root_window, text="Welcome to CherryNpl PEC scraper",
              font=("arial", 16, "bold")).grid(row=1)
        self.next_button.grid(row=2)
        self.root_window.mainloop()

    def search(self):
        self.next_button.destroy()
        self.insert_label.grid(row=2)
        self.tax_input.grid(row=3)
        self.submit_button.grid(row=4)

        self.tax_input.focus_set()

    def validate_input(self, func, code):
        if len(code.get()) == 11:
            self.error_label.grid_forget()
            self.insert_label.grid_forget()
            self.tax_input.grid_forget()
            self.submit_button.grid_forget()

            self.searching_label.grid(row=5)
            self.found = False
            text = Thread(target=self.searching_text, args=(self.searching_label,))
            text.start()

            if func == 'MISSING_KEY':
                self.missing_var()
            pec = func(code.get())
            if pec not in (0, 'MISSING_KEY'):
                print(pec)
                self.found = True
                self.searching_label['text'] = 'TAX: ' + code.get() + ', PEC: ' + pec
            elif pec == 0:
                self.searching_label.grid_forget()
                self.error_label.grid(row=5)
            else:
                self.missing_var()
                return
        else:
            self.searching_label.grid_forget()
            self.error_label.grid(row=5)

        self.tax_input.delete(0, END)
        self.search()

    def missing_var(self):
        self.root_window.geometry("450x150")
        self.searching_label.grid_forget()
        Label(self.root_window, text="Environment variables in the .env file are missing or wrong",
              fg="red", font=("arial", 12)).grid(row=2)

    def thread_runner(self, func):
        Thread(target=self.validate_input, args=(func, self.tax_input)).start()

    def searching_text(self, label):
        while not self.found:
            if label['text'] == 'Searching':
                label['text'] = 'Searching.'
            elif label['text'] == 'Searching.':
                label['text'] = 'Searching..'
            elif label['text'] == 'Searching..':
                label['text'] = 'Searching...'
            elif label['text'] == 'Searching...':
                label['text'] = 'Searching'
            sleep(1)
