"""
This modules contains all code used to render the GUI and make it functional
"""
from Trackers.KeyboardLogger import KeyboardLogger
from Trackers.WindowLogger import WindowLogger
from tkinter import *
from time import strftime
import json


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
        self.session_not_running_text = 'Start Session'
        self.session_running_text = 'Stop Session'
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
        self.start_btn = Button(self.top_frame,
                                text=self.session_not_running_text,
                                command=self.toggle_session, width=15)
        self.start_btn.grid(row=0, sticky='w', padx=5, pady=10)

        self.study_activity = StringVar(self.top_frame)
        self.study_activity.set(self.study_activities[0])
        self.study_activity_menu = OptionMenu(self.top_frame,
                                              self.study_activity,
                                              *self.study_activities)
        self.study_activity_menu.config(width=35)
        self.study_activity_menu.grid(row=0, column=1, pady=10)

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

    # Start running the GUI
    def start(self):
        self.root.mainloop()

    # Toggle tracking session and change the button text
    def toggle_session(self):
        self.session_running = not self.session_running
        if self.session_running:
            self.start_btn.config(text=self.session_running_text)
            self.start_loggers()
        else:
            self.start_btn.config(text=self.session_not_running_text)
            self.stop_loggers()

    # Get study activities for the student from the smartphone app
    # (not implemented yet)
    def get_study_activities(self):
        return ['Read chapter 2', 'Create design doc',
                'Prepare for presentation']

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
