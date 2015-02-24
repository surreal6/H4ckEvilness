# Here, the crawler triggers the requested search for N services (the existing ones).
# Results will be written in the ddbb.
import multiprocessing
from servicesWorker.SingleWorker import FacebookCrawler, SingleWorker


class ServiceWorker(multiprocessing.Process):

    key = None
    value = None
    services = {"fb": "FacebookCrawler",}
    servicesObjs = {}
    model = None

    def run(self):
        jobs = []
        print 'In %s for %s-%s' % (self.name, self.key, self.value)
        self.__init_services()
        # Run all services and join them
        for service in self.servicesObjs.itervalues():
            jobs.append(service)
            service.start()

        for j in jobs:
            j.join()
        print "\tAll crawlers finished"
        return

    def __init__(self, key, value):
        self.key = key
        self.value = value
        super(ServiceWorker, self).__init__()

    def __init_services(self):
        for key, className in self.services.iteritems():
            foo = globals()[className]
            self.servicesObjs[key] = foo(self.key, self.value)