"""
This module allows for the logging of keystrokes
"""

import keyboard


class KeyLogger:

    def __init__(self):
        self.recording = None
        self.key_list = []

    def start_logging(self):
        keyboard.start_recording()

    def stop_logging(self):
        self.recording = keyboard.stop_recording()
        self.convert_log()

    def convert_log(self):
        for keypress in self.recording:
            if keypress.event_type == 'down':
                key = keypress.name
                timestamp = keypress.time
                self.key_list.append([key, timestamp])

    def get_log(self):
        return self.key_list

    def get_info(self):
        return {'name': 'Keyboard Logger', 'description': 'Logs all keyboard pressed during the session.'}
