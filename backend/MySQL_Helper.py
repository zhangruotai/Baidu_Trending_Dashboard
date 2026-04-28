import pymysql


class MySQLHelper:
    def __init__(self, host, port, user, password, database, charset="utf8mb4"):
        self.config = {
            "host": host,
            "port": port,
            "user": user,
            "password": password,
            "database": database,
            "charset": charset,
            "cursorclass": pymysql.cursors.DictCursor
        }

    def get_connection(self):
        return pymysql.connect(**self.config)

    def query_one(self, sql, params=None):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchone()
        finally:
            conn.close()

    def query_all(self, sql, params=None):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                return cursor.fetchall()
        finally:
            conn.close()

    def insert(self, sql, params=None):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.lastrowid
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def update(self, sql, params=None):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                return affected_rows
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()

    def delete(self, sql, params=None):
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                affected_rows = cursor.execute(sql, params)
                conn.commit()
                return affected_rows
        except Exception:
            conn.rollback()
            raise
        finally:
            conn.close()