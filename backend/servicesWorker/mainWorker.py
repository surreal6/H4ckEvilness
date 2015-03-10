# Here, the crawler triggers the requested search for N services (the existing ones).
# Results will be written in the ddbb.
import multiprocessing

from requests.packages import urllib3

from Services.CrossModel import CrossModel
from Services.Github import *
from Services.Twitter import *
from Services.Bing import *
from databases.mainDb import MainDB


class MainWorker(multiprocessing.Process):

    key = None
    value = None
    services = {"bing": "BingCrawler", "github": "GithubCrawler"}
    servicesObjects = {}
    servicesModels = {"tw": TwitterModel(), "gh": GithubModel()}
    cross_model = CrossModel()
    model = None

    def run(self):
        jobs = []
        self.__init_models()
        # self.__init_cross_model()
        self.__init_services()
        self.run_services_and_join(jobs)
        self.set_jobs_results_in_model(jobs)
        self.set_data_in_db()
        print "*** All crawlers finished ***"
        return

    def run_services_and_join(self, jobs):
        # Run all services and join them
        for service in self.servicesObjects.itervalues():
            jobs.append(service)
            service.start()

        for j in jobs:
            j.join()

    def set_jobs_results_in_model(self, jobs):
        for num_jobs in range(len(jobs)):
            result = self.results.get()
            result_services_models = result.get("services", None)
            result_cross_model = result.get("cross", None)
            self.cross_model.mix_results(result_cross_model)
            for key, value in self.servicesModels.iteritems():
                service = result_services_models.get(key, None)
                if service:
                    value.mix_results(service)

    def set_data_in_db(self):
        maindb = MainDB()
        maindb.set_user_status(user_id=self.user_id, status=200)
        maindb.set_services_models(self.user_id, self.servicesModels)
        maindb.set_user_model(self.user_id, self.cross_model)
        maindb.close()

    def __init__(self, key, value, user_id):
        urllib3.disable_warnings()

        self.key = key
        self.value = value
        self.user_id = user_id
        self.tasks = multiprocessing.JoinableQueue()
        self.results = multiprocessing.Queue()
        setattr(self.cross_model, key, value)
        super(MainWorker, self).__init__()

    def __init_models(self):
        self.cross_model.set_user_values(self.user_id)
        for key, service in self.servicesModels.iteritems():
            service.set_user_values(self.user_id)

    def __init_services(self):
        for key, className in self.services.iteritems():
            foo = globals()[className]
            self.servicesObjects[key] = foo(services_models=self.servicesModels.copy(), cross_model=self.cross_model, task_queue=self.tasks, result_queue= self.results)
