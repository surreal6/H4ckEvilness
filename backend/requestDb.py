import sqlite3 as lite
import time


class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]


class RequestDB:
    __metaclass__ = Singleton

    def __init__(self):

        self.dbPath = 'request.db'
        self.con = None
        self.get_connection(self.dbPath)
        query = "CREATE TABLE IF NOT EXISTS Request(HashKey TEXT, Hash TEXT, Cookie TEXT, Status INT, GraphId INT)"
        self.con.cursor().execute(query)

    def get_connection(self, db_path):
        try:
            self.con = lite.connect(db_path)
            print "connection created"
        except lite.Error, e:
            print "Error %s:" % e.args[0]
            # sys.exit(1)

    def query(self, sql):
        rows = []
        try:
            # with self.con:
            cur = self.con.cursor()
            cur.execute(sql)
            # print "the first element in rows will be the column names."
            column_names = [x[0] for x in cur.description]
            rows.append(column_names)
            while True:
                row = cur.fetchone()
                if row is None:
                    break
                rows.append(row)
        except lite.Error, e:
            print "Error %s:" % e.args[0]
        # sys.exit(1)
        return rows

    def get_request_code(self, key, hash):
        try:
            cur = self.con.cursor()
            values = (key, str(hash),)
            row = cur.execute("SELECT * FROM Request WHERE HashKey=? AND Hash=? ", values).fetchall()
            return int(row[0][3])
        except TypeError and IndexError:
            return 202

    def get_request(self, key, hash):
        cur = self.con.cursor()
        values = (key, str(hash),)
        row = cur.execute("SELECT * FROM Request WHERE HashKey=? AND Hash=? ", values).fetchall()
        return row[0]

    def set_request(self, key, hash):
        query_values = (key, str(hash), 'cookie', 202,)
        cur = self.con.cursor()
        cur.execute("INSERT INTO Request VALUES(?,?,?,?, NULL)", query_values)
        self.con.commit()

    def set_request_finished(self, key, hash):
        cur = self.con.cursor()
        cur.execute("UPDATE Request SET Status=200 WHERE HashKey=? AND Hash=? ", (key, str(hash)))
        self.con.commit()

    def remove_request(self, key, hash):
        cur = self.con.cursor()
        cur.execute("DELETE FROM Request WHERE HashKey=? AND Hash=? AND Status=200", (key, str(hash)))
        self.con.commit()
