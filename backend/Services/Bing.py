"""
This is designed for the new Azure Marketplace Bing Search API (released Aug 2012)

Inspired by https://github.com/mlagace/Python-SimpleBing and
http://social.msdn.microsoft.com/Forums/pl-PL/windowsazuretroubleshooting/thread/450293bb-fa86-46ef-be7e-9c18dfb991ad
"""

import requests

from Utils.functions import replace_symbols
from Utils.regex import get_regex_match_group
from servicesWorker.ServiceWorker import ServiceWorker


class BingCrawler(ServiceWorker):
    MSG = "\tRunning bing api search"
    results_rows = []

    def run(self):
        print self.MSG
        params = {'ImageFilters': '"Face:Face"',
                  '$format': 'json',
                  '$top': 50,
                  '$skip': 0}
        self.search_email(self.cross_model.email, params)
        self.search_email_prefix(self.cross_model.email_prefix, params)
        self.process_api_result()
        self.queue_models()

    def search_email(self, email, params):
        request = self.search('web', email, params, exact_match=True).json()
        self.append_results(request)

    def search_email_prefix(self, email_prefix, params):
        request = self.search('web', email_prefix, params, exact_match=True).json()
        self.append_results(request)

    def append_results(self, request):
        try:
            for result in request['d']['results'][0]['Web']:
                self.results_rows.append(result)
        except:
            pass

    def search(self, sources, query, params, exact_match=False):
        request = 'Sources="' + sources + '"'
        request += '&Query="' + str(query) + '"'
        if exact_match:
            request += "&WebSearchOptions='DisableQueryAlterations'"
        for key, value in params.iteritems():
            request += '&' + key + '=' + str(value)
        request = self.url_api + replace_symbols(request)
        return requests.get(request, auth=(self.auth_key, self.auth_key))

    def process_api_result(self):
        num_rows = len(self.results_rows)
        for index, result in enumerate(self.results_rows):
            index_weight = (num_rows-index) / (num_rows*1.0)
            for key, service_model in self.services_models.iteritems():
                if service_model.url_base in result['DisplayUrl']:
                    service_model.put_candidate(result['Url'], index_weight)
                else:
                    matches = get_regex_match_group(service_model.url_profile_rgx, result['Description'])
                    if matches:
                        service_model.put_candidate(matches, index_weight)
                        self.cross_model.put_candidate(result['Url'])