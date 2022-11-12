import os
import pymysql


class Registration:

    def __int__(self):
        pass

    @staticmethod
    def _get_connection():
        usr = os.environ.get("RDS_USERNAME")
        pw = os.environ.get("RDS_PASSWORD")
        h = os.environ.get("RDS_HOSTNAME")
        db = os.environ.get("RDS_DB_NAME")
        port = os.environ.get("RDS_PORT")
        conn = pymysql.connect(
            user=usr,
            password=pw,
            host=h,
            database = db,
            cursorclass=pymysql.cursors.DictCursor,
            autocommit=True
        )
        return conn

    @staticmethod
    def create_user_table():
        sql = ("CREATE TABLE IF NOT EXISTS `registration` ("
        "  `email` varchar(30) NOT NULL ,"
        "  `first_name` varchar(20) NOT NULL,"
        "  `last_name` varchar(20) NOT NULL,"
        "  PRIMARY KEY (`email`)"
        ") ENGINE=InnoDB")

        conn = Registration._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        result = cur.fetchone()
        conn.commit()
        conn.close()
        return result

    @staticmethod
    def get_users():
        sql = "SELECT email, first_name, last_name FROM `registration`"
        conn = Registration._get_connection()
        cur = conn.cursor()
        cur.execute(sql)
        res = cur.fetchall()

        return res

    @staticmethod
    def get_user_record(email):
        sql = "SELECT * FROM `registration` WHERE email = %s"
        val = (email, )
        conn = Registration._get_connection()
        cur = conn.cursor()
        cur.execute(sql, val)
        res = cur.fetchall()

        return res

    @staticmethod

    def add_user(email, fname, lname):
        sql = "INSERT INTO `registration` (email, first_name, last_name) VALUES (%s, %s, %s)"
        conn = Registration._get_connection()
        cur = conn.cursor()
        val = (email, fname, lname)
        try:
            cur.execute(sql, val)
        except(pymysql.err.IntegrityError) as e:

            return e
        finally:
            conn.commit()
            conn.close()
        return None
