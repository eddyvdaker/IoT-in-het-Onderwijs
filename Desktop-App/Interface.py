"""
This modules contains all code used to render the GUI and make it functional.
"""
from Trackers.KeyboardLogger import KeyboardLogger
from Trackers.WindowLogger import WindowLogger
from tkinter import *
from time import strftime, sleep
from threading import Thread
from urllib.request import urlopen
import json

STUDENT_ID = 1
IP = 'ts.guydols.nl'
URL = f'http://{IP}:5000/'


class ScrollableFrame(Frame):

    def __init__(self, master, **kwargs):
        Frame.__init__(self, master, **kwargs)

        # Create canvas object and vertical scrollbar
        self.vscrollbar = Scrollbar(self, orient=VERTICAL)
        self.vscrollbar.pack(side='right', fill='y', expand=False)
        self.canvas = Canvas(self, bg='#dddddd', bd=0, height=350,
                             highlightthickness=0,
                             yscrollcommand=self.vscrollbar.set)
        self.canvas.pack(side='left', fill='both', expand=True)
        self.vscrollbar.config(command=self.canvas.yview)

        # Reset the view
        self.canvas.xview_moveto(0)
        self.canvas.yview_moveto(0)

        # Create frame inside canvas which will be scrolled
        self.interior = Frame(self.canvas, **kwargs)
        self.canvas.create_window(0, 0, window=self.interior, anchor='nw')

        self.bind('<Configure>', self.set_scrollregion)

    def set_scrollregion(self, event=None):
        self.canvas.configure(scrollregion=self.canvas.bbox('all'))


class App:

    def __init__(self):
        # Create class variables
        self.session_running = False
        self.session_not_running_text = 'No session running'
        self.session_running_text = 'Session running'
        self.study_activities = self.get_study_activities()

        # Create list of logger objects
        self.loggers = [KeyboardLogger(), WindowLogger()]
        self.loggers_to_run = []
        self.loggers_to_run_at_start = []

        # Setup GUI root
        self.root = Tk()
        self.root.geometry('400x300')
        self.root.resizable(width=False, height=False)
        self.root.title('StudyBuddy Desktop App')

        # Setup GUI Frames
        self.top_frame = Frame(self.root)
        self.top_frame.pack()
        self.bottom_frame = ScrollableFrame(self.root)
        self.bottom_frame.pack()

        # Setup Top frame
        self.status_label = Label(self.top_frame,
                                  text=self.session_not_running_text,
                                  width=15)

        self.status_label.grid(row=0, sticky='w', padx=5, pady=10)

        # Bottom frame
        for i, logger in enumerate(self.loggers):
            var = IntVar()
            checkbox_text = logger.get_info()['name']
            checkbox = Checkbutton(self.bottom_frame.interior,
                                   text=checkbox_text, variable=var,
                                   width=45, bg='#dddddd', anchor='w',
                                   padx=5, pady=3)
            checkbox.grid(row=i, sticky='w')
            self.loggers_to_run.append(var)

        self.check_thread = Thread(self.check_for_session())

# Start running the GUI
def start(self):
    self.root.mainloop()


# Checks with the API if a session has started for this student
def check_for_session(self):
    while True:
        status = urlopen(f'{URL}?id={STUDENT_ID}')
        status = status.read().decode('utf-8')
        print(status)
        sleep(1)

# Toggle tracking session and change the button text
def toggle_session(self):
    self.session_running = not self.session_running
    if self.session_running:
        self.start_btn.config(text=self.session_running_text)
        self.start_loggers()
    else:
        self.start_btn.config(text=self.session_not_running_text)
        self.stop_loggers()

# Starts each of the loggers that are turned on
def start_loggers(self):
    self.loggers_to_run_at_start = self.loggers_to_run
    for i, logger in enumerate(self.loggers):
        if self.loggers_to_run[i].get() == 1:
            logger.start_logging()

# Stops each of the loggers, starts log collection and log writing
def stop_loggers(self):
    for logger in self.loggers:
        logger.stop_logging()
    logs = self.get_logs()
    self.store_logs(logs)

# Collects the logs from each of the loggers
def get_logs(self):
    logs = {}
    for i, logger in enumerate(self.loggers):
        if self.loggers_to_run_at_start[i].get() == 1:
            logs.update({logger.get_info()['name']: logger.get_log()})
    return logs

# Writes the logs to a results file
def store_logs(self, logs):
    output_file = f'results{strftime("_%Y-%m-%d_%H-%M")}.json'
    with open(output_file, 'w') as file:
        json.dump(logs, file, sort_keys=True, indent=4)
