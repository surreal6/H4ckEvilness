import json
import multiprocessing
import pickle
import time
from Queues.Receiver import ExchangeRpcReceiver
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


class ServiceReceiver(ExchangeRpcReceiver):

    url_api = None
    auth_email = None
    auth_pass = None
    auth_key = None
    _fields = ('url_api', 'auth_email', 'auth_pass', 'auth_key')

    def __init__(self):
        self.cross = None
        self.services = None

        self.set_auth_values()
        super(ServiceReceiver, self).__init__()

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

    def reset_values(self):
        self.cross = None
        self.services = None
        super(ServiceReceiver, self).reset_values()

    def unserialize_message(self, body):
        json_obj = json.loads(body)
        self.cross = pickle.loads(json_obj['cross'])
        self.services = pickle.loads(json_obj['services'])

    def serialize_message(self):
        json_cross = pickle.dumps(self.cross)
        json_services = pickle.dumps(self.services)
        response = {
            "reply_queue": self.queue.method.queue,
            "msg": "It's " + str(int(round(time.time() * 1000))),
            "cross": json_cross,
            "services": json_services
        }
        self.callback_msg = json.dumps(response)