from Metas.DbFieldsReading import DbFieldsReading
from Utils.dictMixing import sym_diff_and_adding_intersection, get_highest_value_key
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
    changed = False

    def __init__(self):
        super(ServiceModel, self).__init__()
        self.candidates_ = dict()
        self.set_auth_values()

    def put_candidate(self, key, weight):
        self.candidates_[key] = self.candidates_.get(key, 0) + 1 + weight

    def mix_results(self, third):
        # print str(third.candidates_)
        # print "Control. Changed %s" % (self.changed,)
        if self.are_new_values_to_update(self.candidates_, third.candidates_):
            intersect = set(self.candidates_.keys()).symmetric_difference(set(third.candidates_.keys()))
            print "\t [+] %s new %s candidates" % (len(intersect), self.__class__.__name__)
        self.changed = self.changed or self.are_new_values_to_update(self.candidates_, third.candidates_)
        # print "Changed %s %s vs %s" % (self.changed, len(self.candidates_.keys()), len(third.candidates_.keys()),)
        self.candidates_ = sym_diff_and_adding_intersection(self.candidates_.copy(),
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

    @staticmethod
    def are_new_values_to_update(dictA, dictB):
        sym_diff = len(set(dictA.keys()).symmetric_difference(set(dictB.keys())))
        # print "\t Sym.Diff values %s" % (sym_diff,)
        return sym_diff is not 0

    def is_changed(self):
        # print self.__class__.__name__+" "+str(self.changed)
        return self.changed

    def reset_changed(self):
        self.changed = False