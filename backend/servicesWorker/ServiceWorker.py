import multiprocessing
from databases.mainDb import MainDB


class ServiceWorker(multiprocessing.Process):

    MSG = 'Running service'
    services_models = {}
    cross_model = None
    url_api = None
    auth_email = None
    auth_pass = None
    auth_key = None
    _fields = ('url_api', 'auth_email', 'auth_pass', 'auth_key')

    def queue_models(self):
        self.result_queue.put({"services": self.services_models, "cross": self.cross_model})

    def get_db_values(self):
        className = self.__class__.__name__
        mainDb = MainDB()
        values = mainDb.get_service_values_by_name(className)
        if values:
            return values
        raise Exception

    def set_auth_values(self):
        try:
            values = self.get_db_values()
            for key, value in values.iteritems():
                if key in self._fields:
                    self.__setattr__(key, value)
        except Exception:
            pass
            # TODO

    def __init__(self, services_models=None, cross_model=None, task_queue=None, result_queue=None):
        self.services_models = services_models
        self.cross_model = cross_model
        self.task_queue = task_queue
        self.result_queue = result_queue
        self.set_auth_values()
        super(ServiceWorker, self).__init__()


class FacebookCrawler(ServiceWorker):

    MSG = "\t\tRunning facebook crawler"

    def run(self):
        super(FacebookCrawler, self).run()
        return
