import pymssql

class Connection:
    def __init__(self):
        self.conn = None

    def connect(self, host_address, u, p, db):
        self.conn = pymssql.connect(server=host_address, user=u, password=p, database=db)
        self.conn.cursor(as_dict=True)
    def close_conn(self):
        self.conn.close()

    def get_conn(self):
        return self.conn
