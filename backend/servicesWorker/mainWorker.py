# Here, the crawler triggers the requested search for N services (the existing ones).
# Results will be written in the ddbb.
import multiprocessing

from requests.packages import urllib3

from Services.CrossModel import CrossModel
from Services.Github import *
from Services.Twitter import *
from Services.Bing import *
from databases.mainDb import MainDB
from servicesWorker.ServiceWorker import ServiceWorker

class MainWorker(multiprocessing.Process):

    key = None
    value = None
    services = {"bing": "BingCrawler"}
    servicesObjs = {}
    servicesModels = {"tw": TwitterModel(), "gh": GithubModel()}
    cross_model = CrossModel()
    model = None

    def run(self):
        jobs = []
        self.__init_services()
        # Run all services and join them
        for service in self.servicesObjs.itervalues():
            jobs.append(service)
            service.start()

        for j in jobs:
            j.join()

        for num_jobs in range(len(jobs)):
            result = self.results.get()
            servicesModels_ = result.get("services", None)
            cross_model_ = result.get("cross", None)
            self.cross_model.mix_results(cross_model_)
            for key, value in self.servicesModels.iteritems():
                service = servicesModels_.get(key, None)
                if service:
                    value.mix_results(service)

        print "\tAll crawlers finished"
        maindb = MainDB()
        maindb.set_user_status(user_id=self.user_id, status=200)
        return

    def __init__(self, key, value, user_id):
        urllib3.disable_warnings()

        self.key = key
        self.value = value
        self.user_id = user_id
        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()
        setattr(self.cross_model, key, value)
        super(MainWorker, self).__init__()

    def __init_services(self):
        for key, className in self.services.iteritems():
            foo = globals()[className]
            self.servicesObjs[key] = foo(services_models=self.servicesModels.copy(), cross_model=self.cross_model, task_queue=self.tasks, result_queue= self.results)

    def __del__(self):
        print "__del"