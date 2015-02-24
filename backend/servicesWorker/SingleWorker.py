import multiprocessing


class SingleWorker(multiprocessing.Process):

    key = None
    value = None
    services = []
    model = None

    def run(self):
        print 'Running service'
        return

    def __init__(self, key, value):
        self.key = key
        self.value = value
        super(SingleWorker, self).__init__()


class FacebookCrawler(SingleWorker):

    MSG = "\t\tRunning facebook crawler"

    def run(self):
        print self.MSG
        return