"""
This modules contains all code used to render the GUI and make it functional.
"""
from Trackers.KeyboardLogger import KeyboardLogger
from Trackers.WindowLogger import WindowLogger
from tkinter import *
from time import strftime
from urllib.request import urlopen, Request
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
        self.session_id = None

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
        self.status_label = Label(self.top_frame, text=f'Session stopped',
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

    def check_api(self):
        status = urlopen(f'{URL}check_session?id={STUDENT_ID}')
        status = json.loads(status.read().decode('utf-8'))['id']
        print(f'\nID from API: {status} - Local ID: {self.session_id}')
        print(f'Loggers to run: {[x.get() for x in self.loggers_to_run]}')

        if not status and self.session_id:
            print('Stopping loggers...')
            self.toggle_session()
        elif status and not self.session_id:
            print('Starting loggers...')
            self.toggle_session()
        elif status and self.session_id and status != self.session_id:
            print('Restarting loggers...')
            self.toggle_session()
            self.toggle_session()
        else:
            print('No changes...')

        self.session_id = status
        self.root.after(2000, self.check_api)

    # Start running the GUI
    def start(self):
        self.root.after(0, self.check_api)
        self.root.mainloop()

    # Toggle tracking session and change the button text
    def toggle_session(self):
        self.session_running = not self.session_running
        if self.session_running:
            self.status_label.config(text='Session running')
            self.start_loggers()
        else:
            self.status_label.config(text='Session stopped')
            self.stop_loggers()

    # Starts each of the loggers that are turned on
    def start_loggers(self):
        self.loggers_to_run_at_start = self.loggers_to_run
        for i, logger in enumerate(self.loggers):
            if self.loggers_to_run[i].get() == 1:
                logger.start_logging()

    # Stops each of the loggers, starts log collection and log writing
    def stop_loggers(self):
        for i, logger in enumerate(self.loggers):
            if self.loggers_to_run_at_start[i].get() == 1:
                logger.stop_logging()
        logs = self.get_logs()
        self.store_logs(logs)

    # Collects the logs from each of the loggers
    def get_logs(self):
        logs = []
        for i, logger in enumerate(self.loggers):
            if self.loggers_to_run_at_start[i].get() == 1:
                info = logger.get_info()
                session_data = str({info['name']: logger.get_log()})
                logs.append({'data_type': info['data type'],
                             'sessiondata': session_data,
                             'sessionid': self.session_id})
        return logs

    # Writes the logs to a results file
    def store_logs(self, logs):
        for log in logs:
            req = Request(f'{URL}upload_data')
            req.add_header('Content-Type', 'application/json; charset=utf-8')
            json_data = json.dumps(log).encode('utf-8')
            req.add_header('Content-Length', len(json_data))
            urlopen(req, json_data)
