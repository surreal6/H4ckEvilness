from Metas.DbFieldsReading import DbFieldsReading
from Utils.dictMixing import sym_diff_and_adding_intersec, get_highest_value_key
from databases.mainDb import MainDB


class ServiceModel(DbFieldsReading):
    _fields = ('url_base', 'url_profile_rgx', 'id')
    _user_fields = ('url_profile', 'nick', 'nick_id')

    url_profile = None
    url_profile_rgx = None
    url_base = None
    id = None

    nick = None
    nick_id = None
    candidates_ = {}

    def __init__(self):
        super(ServiceModel, self).__init__()
        self.candidates_ = dict()
        self.set_auth_values()

    def put_candidate(self, key, weight):
        self.candidates_[key] = self.candidates_.get(key, 0) + 1 + weight

    def mix_results(self, third):
        self.candidates_ = sym_diff_and_adding_intersec(self.candidates_.copy(),
                                                        third.candidates_.copy())
        self.populate_candidate()

    def populate_candidate(self):
        self.url_profile = get_highest_value_key(self.candidates_)

    def get_auth_db_values(self):
        _class_name = self.__class__.__name__
        maindb = MainDB()
        values = maindb.get_service_values_by_model_name(_class_name)
        if values:
            return values
        raise Exception

    def set_auth_values(self):
        try:
            values = self.get_auth_db_values()
            for key, value in values.iteritems():
                if key in self._fields:
                    self.__setattr__(key, value)
        except Exception:
            pass
            # TODO

    def get_user_values(self, user_id=None):
        maindb = MainDB()
        return maindb.get_service_model(user_id, self)