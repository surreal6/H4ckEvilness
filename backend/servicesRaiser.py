import sys
import multiprocessing as mp
import signal
import time
from requests.packages import urllib3

from Services.Github import *
from Services.Twitter import *
from Services.Bing import *


def raise_rpc_receiver(key, value):
    foo = globals()[value]
    foo()


def signal_handler(signal, frame):
    print 'You pressed Ctrl+C!'
    sys.exit(0)

servicesDict = {"twitter": "TwitterCrawler", "github": "GithubRPCCrawler", "bing": "BingCrawler"}


if __name__ == '__main__':
    urllib3.disable_warnings()

    for key, value in servicesDict.iteritems():
        p = mp.Process(target=raise_rpc_receiver, args=(key, value,))
        p.start()

    signal.signal(signal.SIGINT, signal_handler)
    while True:
        time.sleep(1)