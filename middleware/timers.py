import time
import threading

def sleep(seconds):
    time.sleep(seconds)

def set_interval(interval, action, *args, **kwargs):
    def wrapper():
        while True:
            time.sleep(interval)
            action(*args, **kwargs)
    thread = threading.Thread(target=wrapper)
    thread.start()
    return thread