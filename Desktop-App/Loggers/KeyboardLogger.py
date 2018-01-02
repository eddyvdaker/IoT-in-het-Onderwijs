import keyboard


class KeyLogger:

    def __init__(self):
        self.recording = None
        self.key_list = []
        self.key_frequency = {}

    def start_logging(self):
        keyboard.start_recording()

    def stop_logging(self):
        self.recording = keyboard.stop_recording()
        self.convert_log()

    def convert_log(self):
        for keypress in self.recording:
            if 'down' in str(keypress):
                current_key = str(keypress)[14:-6]

                self.key_list.append(current_key)

                if current_key in self.key_frequency:
                    self.key_frequency[current_key] += 1
                else:
                    self.key_frequency.update({current_key: 1})

    def get_log(self):
        return [self.key_list, self.key_frequency]
