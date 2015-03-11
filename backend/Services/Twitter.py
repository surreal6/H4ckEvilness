import requests
from Services.ServiceModel import ServiceModel
from Utils import functions
from servicesWorker.ServiceWorker import ServiceWorker


class TwitterModel(ServiceModel):

    def populate_candidate(self):
        super(TwitterModel, self).populate_candidate()
        if self.url_profile:
            self.nick = self.url_profile[self.url_profile.rfind("/")+1:]


class TwitterCrawler(ServiceWorker):

    MSG = "\tRan twitter\'s crawler"

    def run(self):
        print self.MSG
        self.crawl_name()
        self.queue_models()
        super(TwitterCrawler, self).run()

    def crawl_name(self):
        this_service = self.services_models['tw']
        if this_service and this_service.url_profile:
            print "\t\tLooking for user name"
            if "http" not in this_service.url_profile:
                url_name = "http://"+this_service.url_profile
            else:
                url_name = this_service.url_profile
            r = requests.get(url_name)
            checkedName = False
            for line in r.iter_lines():
                if checkedName:
                    name = functions.get_tag_value(line)
                    self.cross_model.put_name_candidate(name)
                    break
                if line and ("ProfileHeaderCard-nameLink" in line):
                    checkedName = True
        pass
