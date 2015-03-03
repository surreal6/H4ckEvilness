from databases.mainDb import MainDB


class ServiceModel(object):

    _fields = ('url_base', 'url_profile_rgx',)

    url_profile = None
    url_profile_rgx = None
    url_base = None

    id = None
    nick = None
    candidates_ = {}

    def __init__(self):
        self.candidates_ = dict()
        self.set_auth_values()
        pass

    def put_candidate(self, key, weight):
        self.candidates_[key] = self.candidates_.get(key, 0) + 1 + weight

    def mix_results(self, third):
        self.candidates_.update(third.candidates_)
        self.populate_candidate()

    def populate_candidate(self):
        final_candidate = None
        final_candidate_value = 0
        for key, value in self.candidates_.iteritems():
            if value > final_candidate_value:
                final_candidate = key
                final_candidate_value = value
        self.url_profile = final_candidate

    def get_db_values(self):
        className = self.__class__.__name__
        mainDb = MainDB()
        values = mainDb.get_service_values_by_model_name(className)
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