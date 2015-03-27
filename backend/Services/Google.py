import requests
from Utils.functions import replace_symbols, replace_symbols_bis
from servicesWorker.ServiceWorker import ServiceReceiver
from pyquery import PyQuery as pq
from BeautifulSoup import BeautifulSoup as Soup
from beautifulsoupselect import select

class GoogleCrawler(ServiceReceiver):

    user_agent = "NokiaN97i/SymbianOS/9.1 Series60/3.0"
    headers = {
        'User-Agent': user_agent,
    }
    results_rows = []

    def init_task(self):
        self.results_rows = []
        results = self.search_email()
        self.append_results(results)
        self.process_api_result()

    def search_email(self):
        request = "q=\"" + self.cross.email + "\""
        request = self.url_api + replace_symbols_bis(request)
        response = requests.get(request, headers=self.headers)

        # soup = Soup(response.text)
        # links = select(soup, 'div.web_result > div > a')
        #
        # for link in links:
        #     title = link.string
        #     href = link.get('href')
        d = pq(str(response.text))
        returno = d(".web_result > div > div > span")
        return returno

    def append_results(self, request):
        try:
            for result in request:
                self.results_rows.append(result.text)
        except:
            pass

    def process_api_result(self):
        num_rows = len(self.results_rows)
        for index, result in enumerate(self.results_rows):
            index_weight = (num_rows-index) / (num_rows*1.0)
            for key, service_model in self.services.iteritems():
                if service_model.url_base in result:
                    service_model.put_candidate(result, index_weight)
