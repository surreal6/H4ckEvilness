
class CrossModel(object):

    email = None
    email_prefix = None
    name = None
    phone = None
    photo = None
    national_id = None
    names_ = {}
    emails_ = {}
    diff_urls = {}

    def __init__(self):
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

    def put_candidate(self, key):
        self.diff_urls[key] = self.diff_urls.get(key, 0) + 1

    def mix_results(self, third):
        self.diff_urls.update(third.diff_urls)
        self.emails_.update(third.emails_)
        self.names_.update(third.names_)
        # self.populate_name()
        # self.populate_email()
