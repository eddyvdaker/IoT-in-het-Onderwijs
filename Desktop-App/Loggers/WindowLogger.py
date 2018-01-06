"""
This module allows for the logging of the opened windows and window titles
"""

from ctypes import *
import threading
import time


class WindowLogger:

    def __init__(self):
        self.user32 = windll.user32
        self.kernel32 = windll.kernel32
        self.psapi = windll.psapi
        self.current_window = None

        self.running = False
        self.windows_log = []

    def start_logging(self):
        self.running = True
        thread = threading.Thread(target=self.logging, args=[])
        thread.start()

    def stop_logging(self):
        self.running = False

    def get_log(self):
        return self.windows_log

    def get_info(self):
        return {'name': 'Window Logger',
                'description': 'Logs the windows opened during the session.'}

    def logging(self):
        while self.running:
            time.sleep(1)
            new_window = self.get_current_process().decode('utf-8')

            if new_window == self.current_window:
                pass
            elif new_window == '':
                pass
            elif 'Opening - ' in new_window:
                pass
            else:
                self.current_window = new_window
                self.windows_log.append([new_window, time.time()])

    def get_current_process(self):
        foreground_handle = self.user32.GetForegroundWindow()

        # Get process ID
        pid = c_ulong(0)
        self.user32.GetWindowThreadProcessId(foreground_handle, byref(pid))
        process_id = "%d" % pid.value

        # Get executable
        executable = create_string_buffer(b"\x00" * 512)
        h_process = self.kernel32.OpenProcess(0x400 | 0x10, False, pid)
        self.psapi.GetModuleBaseNameA(h_process, None, byref(executable), 512)

        # Read window title
        window_title = create_string_buffer(b"\x00" * 512)
        length = self.user32.GetWindowTextA(foreground_handle,
                                            byref(window_title), 512)

        self.kernel32.CloseHandle(foreground_handle)
        self.kernel32.CloseHandle(h_process)

        return window_title.value
