import god.checker as checker

from urllib.request import urlopen, URLError

thread = None
state = 'idle'


def check_internet():
    try:
        urlopen('http://google.com', timeout=5)
        return True
    except URLError:
        return False


def start():
    global thread
    thread = checker.Thread()
    thread.start()


def stop():
    thread.kill()
