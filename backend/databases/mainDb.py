from itertools import cycle
import psycopg2
from psycopg2._psycopg import InternalError
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
            self.conn = psycopg2.connect(database=_dbname, user=_user, host=_host, password=_pass)
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
        return self.select(query, values=values)

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
