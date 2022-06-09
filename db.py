from sqlalchemy import create_engine, exc
import os
import helper as helper


class Database():
    def __init__(self):
    #Make sure to set env vars with username and pw on your machine
        pw = os.getenv('PW_DB', "password")
        user = os.getenv('USER_DB', "julianserra")
        dbhost = os.getenv('DATABASE_URL', "127.0.0.1:5432")
        dbname = os.getenv("DB_NAME", "shirts_qr")
        database_string = 'postgres://%s:%s@%s/%s' % (user, pw, dbhost, dbname)
        db_string = os.getenv('DATABASE_URL', database_string)

        self.engine = create_engine(db_string)
        self.connection = None

    def create_connection(self):
        self.connection = self.engine.connect()

    def close_connection(self):
        self.connection.close()

    def execute_query(self, q):
        self.engine.execute(q)

    def create_user(self, email, pw, first_name, last_name):
        #hash the password for storage
        pw = helper.hash_password(pw)
        sql = "INSERT INTO users (email, password, first_name, last_name)  VALUES ('%s','%s','%s','%s') RETURNING user_id" % (email, pw, first_name, last_name)
        try:
            result = self.connection.execute(sql)
            id = result.fetchone()[0]
            return id
        except exc.IntegrityError as e:
            print("user exists")
            return False

    def set_shirt_qr(self, shirt_id, qr_id):
        sql = "UPDATE shirts set qr_id='%s' where shirt_id=%s" % (qr_id, shirt_id)
        print(sql)
        try:
            result = self.connection.execute(sql)
            return True
        except exc.IntegrityError as e:
            print("shirt exists")
            return False

    def create_shirt(self, user_id, name, text, url, status, image_id):
        sql = "INSERT INTO shirts (user_id, name, text_content, redirect_url, status, image_id)  VALUES (%d,'%s','%s','%s','%s','%s') RETURNING shirt_id" % (user_id, name, text, url, status, image_id)
        try:
            result = self.connection.execute(sql)
            id = result.fetchone()[0]
            qr_id = helper.getQrId(id)
            self.set_shirt_qr(id, qr_id)
            return id
        except exc.IntegrityError as e:
            print("shirt exists")
            return False

    def update_shirt(self, shirt_id, name, text, url, image_id):
        sql = "UPDATE shirts set name='%s', text_content='%s', redirect_url='%s', image_id='%s' where shirt_id=%s" % (name, text, url, image_id, shirt_id)
        print(sql)
        try:
            result = self.connection.execute(sql)
            return True
        except exc.IntegrityError as e:
            print("shirt exists")
            return False



    def get_user(self, email):
        q = "SELECT * FROM USERS where email='%s'" % email
        result = self.connection.execute(q)

        for r in result:
            d = dict(r)
            self.userId = d["user_id"]
            self.email = d["email"]
            return d

    def get_shirt(self, shirt_id):
        q = "SELECT * FROM shirts where shirt_id='%s'" % shirt_id
        result = self.connection.execute(q)

        for r in result:
            d = dict(r)
            return d

    def get_user_shirts(self, user_id):
        q = "SELECT * FROM shirts where user_id='%s'" % user_id
        result = self.connection.execute(q)
        l = []
        for r in result:
            d = dict(r)
            l.append(d)
        return l

    def delete_shirt(self, shirt_id):
        q = "DELETE FROM shirts where shirt_id='%s'" % shirt_id
        result = self.connection.execute(q)
        return result

    def login(self, email, pw):
        q = "SELECT * FROM USERS where email='%s'" % email
        result = self.connection.execute(q)
        if(result):
            for r in result:
                d = dict(r)
                self.userId = d["user_id"]
                self.email = d["email"]
                return helper.verify_password(d["password"], pw)

        return False
