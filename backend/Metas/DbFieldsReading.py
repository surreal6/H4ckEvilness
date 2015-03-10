
class DbFieldsReading(object):
    @property
    def _user_fields(self):
        raise NotImplementedError

    def __init__(self):
        super(DbFieldsReading, self).__init__()

    def get_user_values(self, user_id=None):
        raise NotImplementedError

    def set_user_values(self, user_id=None):
        try:
            values = self.get_user_values(user_id)
            for key, value in values.iteritems():
                if key in self._user_fields:
                    self.__setattr__(key, value)
        except Exception:
            pass
