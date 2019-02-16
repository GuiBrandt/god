import god.checker as checker

from urllib.request import urlopen, URLError

god_thread = None


def check_internet():
    try:
        urlopen('http://google.com', timeout=5)
        return True
    except URLError:
        return False


def start():
    global god_thread
    god_thread = checker.Thread()
    god_thread.start()


def stop():
    god_thread.kill()
