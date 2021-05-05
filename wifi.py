from urllib.request import urlopen
import speedtest
def is_internet_available():
    try:
        urlopen('http://216.58.192.142', timeout=1)
        return True
    except:
        return False

def get_download_speed():
    if is_internet_available():
        s = speedtest.Speedtest()
        speed = s.download()
        speed /= 1000000
        return int(speed)
    else:
        return 0
