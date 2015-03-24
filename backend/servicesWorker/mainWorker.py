# Here, the crawler triggers the requested search for N services (the existing ones).
# Results will be written in the ddbb.
import json
import multiprocessing
import pickle

from requests.packages import urllib3
from Queues.Emit import ExchangeRpcWorker

from Services.CrossModel import CrossModel
from Services.Github import *
from Services.Twitter import *
from Services.Bing import *
from databases.mainDb import MainDB
from servicesRaiser import servicesDict


class MainWorker(multiprocessing.Process, ExchangeRpcWorker):

    key = None
    value = None
    services = {"bing": "BingCrawler", "github": "GithubCrawler", "twitter": "TwitterCrawler"}
    servicesObjects = {}
    servicesModels = {"tw": TwitterModel(), "gh": GithubModel()}
    cross_model = CrossModel()
    model = None

    def __init__(self, key, value, user_id):
        urllib3.disable_warnings()

        self.key = key
        self.value = value
        self.user_id = user_id
        self.callback_count = 0
        setattr(self.cross_model, key, value)
        super(MainWorker, self).__init__()

    def run(self):
        self.set_models_from_db()

        self.connect()
        self.declare_queues()

        self.serialize_body_msg()
        self.publish()
        self.wait_responses()
        #self.set_results_in_instance() inside wait_response > on_emit_callback() >
        self.set_results_in_db()
        print " [x] All crawlers finished"
        return

    #Mixes existing values with coming ones.
    def set_results_in_instance(self, body):
        callback_result = self.unserialize_body_msg(body)
        result_services_models = callback_result.get("services", None)
        result_cross_model = callback_result.get("cross", None)
        reply_queue = callback_result.get("reply_queue")

        print "Reply queue %s" % (reply_queue,)
        self.cross_model.mix_results(result_cross_model)
        for key, value in self.servicesModels.iteritems():
            service = result_services_models.get(key, None)
            if service:
                value.mix_results(service)
        self.cross_model.populate_name()

    def set_results_in_db(self):
        maindb = MainDB()
        maindb.set_user_status(user_id=self.user_id, status=200)
        maindb.set_services_models(self.user_id, self.servicesModels)
        maindb.set_user_model(self.user_id, self.cross_model)
        maindb.close()

    def check_stop_condition(self):
        self.callback_count += 1
        if self.callback_count >= len(servicesDict):
            self.stop_consuming()

    def serialize_body_msg(self):
        json_cross = pickle.dumps(self.cross_model)
        json_services = pickle.dumps(self.servicesModels)
        return json.dumps({
            "msg": "self.msg",
            "exchange_str": self.callback_queue.method.queue,
            "cross": json_cross,
            "services": json_services,
        })

    def unserialize_body_msg(self, body):
        json_obj = json.loads(body)
        cross = pickle.loads(json_obj['cross'])
        services = pickle.loads(json_obj['services'])

        return {
            "cross": cross,
            "reply_queue": json_obj['reply_queue'],
            "services": services,
            "msg": json_obj['msg'],
        }

    def set_models_from_db(self):
        self.cross_model.set_user_values(self.user_id)
        for key, service in self.servicesModels.iteritems():
            service.set_user_values(self.user_id)
