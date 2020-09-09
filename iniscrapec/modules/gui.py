from threading import Thread
from time import sleep
from tkinter import Tk, Label, Entry, Button, END


class RootWindow:
    """
    Class used to manage the main gui window
    """
    def __init__(self, func):
        # Standard configuration
        self.root_window = Tk()
        self.root_window.title("TAXtoPEC - CherryNpl")
        self.root_window.geometry("380x150")

        # If some key was missing from environment it just shows an error code
        if func == 'MISSING_KEY':
            self.root_window.geometry("450x150")
            Label(self.root_window,
                  text="Environment variables in the .env file are missing or wrong",
                  fg="red", font=("arial", 12)).grid(row=1)
            self.root_window.mainloop()

        # Creation of all the needed labels and input
        else:
            self.searching_label = Label(self.root_window,
                                         text="Searching...",
                                         font=("arial", 12))
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
        """ Creates first interface"""
        Label(self.root_window, text="Welcome to CherryNpl PEC scraper",
              font=("arial", 16, "bold")).grid(row=1)
        self.next_button.grid(row=2)
        self.root_window.mainloop()

    def search(self):
        """ Creates the searching interface where to put the TAX code"""
        self.next_button.destroy()
        self.insert_label.grid(row=2)
        self.tax_input.grid(row=3)
        self.submit_button.grid(row=4)

        self.tax_input.focus_set()

    def validate_input(self, func, code):
        """ Checks if the TAX code is valid and call the func passed in the parameter
            (usually the scraping function)"""
        if len(code.get()) == 11:
            # Hides the interface to write a simple "Searching" animation
            self.error_label.grid_forget()
            self.insert_label.grid_forget()
            self.tax_input.grid_forget()
            self.submit_button.grid_forget()

            self.searching_label.grid(row=5)
            self.found = False
            text = Thread(target=self.searching_text, args=(self.searching_label,))
            text.start()

            # If some key was deleted or wrong shows the error message
            if func == 'MISSING_KEY':
                self.missing_var()
            # Actual computing of the code
            pec = func(code.get())
            if pec not in (0, 'MISSING_KEY'):
                # No errors path
                print(pec)
                self.found = True
                self.searching_label['text'] = 'TAX: ' + code.get() + ', PEC: ' + pec
            elif pec == 0:
                # No PEC found, probably the TAX was wrong
                self.searching_label.grid_forget()
                self.error_label.grid(row=5)
            else:
                # If some key was deleted or wrong shows the error message
                self.missing_var()
                return
        else:
            # The code was invalid
            self.searching_label.grid_forget()
            self.error_label.grid(row=5)

        self.tax_input.delete(0, END)
        # Recreate the input interface
        self.search()

    def missing_var(self):
        """ Function that stop the computation and shows an error about environment variables"""
        self.root_window.geometry("450x150")
        self.searching_label.grid_forget()
        Label(self.root_window, text="Environment variables in the .env file are missing or wrong",
              fg="red", font=("arial", 12)).grid(row=2)

    def thread_runner(self, func):
        """ Simple thread used to compute the TAX code multiple times without stopping the interface"""
        Thread(target=self.validate_input, args=(func, self.tax_input)).start()

    def searching_text(self, label):
        """ Simple text animation """
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
