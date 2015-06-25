from itertools import cycle
import psycopg2
from psycopg2._psycopg import InternalError, IntegrityError
from Metas.Patterns import Singleton

_dbname = 'evilDatabase'
_user = 'maligno'
_host = 'localhost'
_pass = 'ePvP4quXsHvp'


class MainDB:
    __metaclass__ = Singleton

    def __init__(self):
        self.get_connection()

    def __del__(self):
        print "Closing connection"
        self.conn.close()

    def get_connection(self):
        try:
            self.close()
            self.conn = psycopg2.connect(database=_dbname, user=_user, host=_host) #, password=_pass)
        except Exception as e:
            print "I am unable to connect to the database "+e.message

    def close(self):
        try:
            self.conn.close()
        except AttributeError:
            pass

    def select(self, query, values=None):
        self.get_connection()
        try:
            return self.__select(query, values)
        except InternalError:
            self.conn.rollback()
            return self.__select(query, values)

    def __select(self, query, values):
        rows = []
        cursor = self.conn.cursor()
        if values:
            cursor.execute(query, values)
        else:
            cursor.execute(query)
        column_names = [x[0] for x in cursor.description]
        # rows.append(column_names)
        while True:
            row = cursor.fetchone()
            if row is None:
                break
            li_row = cycle(row)
            row_dict = {}
            for key in column_names:
                row_dict[key] = li_row.next()
            rows.append(row_dict)
        return rows[0] if len(rows) == 1 else rows

    def insert(self, query, values=None):
        self.get_connection()
        try:
            return self.__insert(query, values)
        except InternalError:
            self.conn.rollback()
            return self.__insert(query, values)

    def __insert(self, query, values):
        cur = self.conn.cursor()
        cur.execute(query, values)
        self.conn.commit()
        return cur.fetchone()

    def is_user_in_db(self, email=None):
        if email:
            user_by_email = self.get_user_by_email(email)
            return user_by_email and len(user_by_email) is not 0

    def get_user(self, user_email=None, user_id=-1):
        if user_email:
            return self.get_user_by_email(user_email)
        elif user_id is not -1:
            return self.get_user_by_id(user_id)

    def get_user_by_email(self, email_in):
        query = "SELECT * FROM users where email = %s"
        values = (email_in,)
        return self.select(query, values)

    def get_user_by_id(self, user_id):
        query = "SELECT * FROM users where id = %s"
        values = (user_id,)
        user_data = self.select(query, values=values)
        user_data['services'] = self.get_services_data(user_id)
        return user_data

    def get_services_data(self, user_id):
        query = "select user_services.url_profile, user_services.nick, user_services.nick_id, services.s_name from user_services left join services on user_services.service_fk=services.id where user_services.user_fk=%s"
        values = (user_id,)
        result = self.select(query, values)
        returno = {}
        for service in result:
            try:
                key = service['s_name']
                del service['s_name']
                returno[key] = service
            except TypeError:
                pass
        return returno

    def put_user_by_email(self, email_in):
        query = "INSERT INTO users(email) VALUES(%s) RETURNING id"
        values = (email_in,)
        #Returns user's id.
        return self.insert(query, values)[0]

    def set_user_updating(self, user_id=0):
        query = "update users set status=204 where id = %s RETURNING id"
        values = (user_id,)
        #Returns user's id.
        return self.insert(query, values)[0]

    def set_user_status(self, user_id=None, status=202):
        if user_id:
            query = "update users set status=%s where id = %s RETURNING id"
            values = (status, user_id,)
            #Returns user's id.
            return self.insert(query, values)[0]

    def get_service_values_by_name(self, s_name=None):
        query = "SELECT * FROM services where crawler_name = %s LIMIT 1"
        values = (s_name,)
        return self.select(query, values)

    def get_service_values_by_model_name(self, s_name=None):
        query = "SELECT * FROM services where model_name = %s LIMIT 1"
        values = (s_name,)
        return self.select(query, values)

    def set_services_models(self, user_id, services):
        for key, service in services.iteritems():
            try:
                self.insert_service_model(user_id, service)
            except IntegrityError:
                self.update_service_model(user_id, service)

    def insert_service_model(self, user_id, service):
        query = "INSERT INTO user_services(user_fk, service_fk, url_profile, nick) VALUES(%s, %s, %s, %s) RETURNING user_fk"
        values = (
            int(user_id),
            int(service.id),
            service.url_profile,
            service.nick,
        )
        result = self.insert(query, values)[0]

    def update_service_model(self, user_id, service):
        query = "update user_services set url_profile=%s, nick=%s where user_fk=%s and service_fk=%s RETURNING user_fk"
        values = (
            service.url_profile,
            service.nick,
            int(user_id),
            int(service.id),
        )
        result = self.insert(query, values)[0]

    def get_service_model(self, user_id, service):
        query = "SELECT * FROM user_services where user_fk=%s and service_fk=%s"
        values = (
            int(user_id),
            int(service.id),
        )
        return self.select(query, values)

    def set_user_model(self, user_id, user_model):
        query = "update users set name=%s where id=%s RETURNING id"
        values = (
            user_model.name,
            int(user_id),
        )
        result = self.insert(query, values)[0]