import time
import os
import os.path


def error(location, exception):
    with open("error.log", "a") as log_file:
        timestamp = time.ctime(time.time())
        log_file.write(f"<{timestamp} at `{location}`> {exception}\n")
