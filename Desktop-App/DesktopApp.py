"""
Starts the application
"""
from Loggers import KeyboardLogger

from time import sleep


if __name__ == '__main__':
    kl = KeyboardLogger.KeyLogger()
    kl.start_logging()
    sleep(10)
    kl.stop_logging()
    sleep(1)
    logs = kl.get_log()

    print(logs[0])
    print()
    print(logs[1])
