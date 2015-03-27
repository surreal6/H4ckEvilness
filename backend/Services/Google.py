import requests
from pyquery import PyQuery as pq

from Utils.functions import replace_symbols_bis
from servicesWorker.ServiceWorker import ServiceReceiver


class GoogleCrawler(ServiceReceiver):

    user_agent = "NokiaN97i/SymbianOS/9.1 Series60/3.0"
    headers = {
        'User-Agent': user_agent,
    }
    results_rows = []

    def init_task(self):
        self.results_rows = []
        self.search_by_email_twitter()
        self.search_by_email_github()
        self.search_by_email_broad()
        self.process_api_result()

    def search_by_email_broad(self):
        print " [x] %s | Searching email \"%s\"" % (self.queue.method.queue, self.cross.email, )
        results = self.search("\"" + self.cross.email + "\"")
        self.append_results(results)

    def search_by_email_twitter(self):
        if self.cross.name and self.cross.email:
            print " [x] %s | Searching twitter \"%s\"" % (self.queue.method.queue, self.cross.email, )
            results = self.search("twitter " + self.cross.name + " " + self.cross.email)
            self.append_results(results)

    def search_by_email_github(self):
        if self.cross.name and self.cross.email:
            print " [x] %s | Searching github \"%s\"" % (self.queue.method.queue, self.cross.email, )
            results = self.search("github " + self.cross.name + " " + self.cross.email)
            self.append_results(results)

    def search(self, query):
        request = "q=" + query
        request = self.url_api + replace_symbols_bis(request)
        response = requests.get(request, headers=self.headers)
        d = pq(str(response.text))
        return d(".web_result > div > div > span")

    def append_results(self, request):
        try:
            for result in request:
                self.results_rows.append(result.text)
        except:
            pass

    def process_api_result(self):
        num_rows = len(self.results_rows)
        # print "Up to proccess %s results" % (num_rows,)
        for index, result in enumerate(self.results_rows):
            index_weight = (num_rows-index) / (num_rows*1.0)
            for key, service_model in self.services.iteritems():
                if service_model.url_base in result:
                    service_model.put_candidate(result, index_weight)
