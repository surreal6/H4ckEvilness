from Metas.DbFieldsReading import DbFieldsReading
from databases.mainDb import MainDB


class CrossModel(DbFieldsReading):

    email = None
    email_prefix = None
    name = None
    phone = None
    photo = None
    national_id = None
    names_ = {}
    emails_ = {}
    diff_urls = {}
    _user_fields = ('email', 'name')

    def __init__(self, user_id=None):
        super(CrossModel, self).__init__()
        if user_id:
            pass
        self.diff_urls = dict()
        self.emails_ = dict()
        self.names_ = dict()
        pass

    def __setattr__(self, name, value):
        if name is "email":
            self.__dict__[name] = value
            self.email_prefix = value.split("@")[0]
        else:
            super(CrossModel, self).__setattr__(name, value)

    def put_name_candidate(self, key):
        self.names_[key] = self.names_.get(key, 0) + 1

    def put_candidate(self, key):
        self.diff_urls[key] = self.diff_urls.get(key, 0) + 1

    def mix_results(self, third):
        self.diff_urls.update(third.diff_urls)
        self.emails_.update(third.emails_)
        self.names_.update(third.names_)

    def populate_name(self):
        final_candidate = None
        final_candidate_value = 0
        for key, value in self.names_.iteritems():
            if value > final_candidate_value:
                final_candidate = key
                final_candidate_value = value
        self.name = final_candidate
        if self.name:
            print "** Name> "+self.name +"("+str(final_candidate_value)+")"

    def get_user_values(self, user_id=None):
        maindb = MainDB()
        return maindb.get_user(self, user_id=user_id)