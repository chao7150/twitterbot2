import mysql.connector
import profile

class Database:

    def __init__(self):
        self.dbh = mysql.connector.connect(
            host = profile.HOST,
            db = profile.DB,
            user = profile.USER,
            password = profile.PASSWORD
        )
        self.cur = self.dbh.cursor(buffered = True)

    def insert(self, r):
        print(r)
        if self.hashcheck(r[0]) == 0:
            sql = "insert into memory values(%s, %s, %s, %s, %s)"
            try:
                self.cur.execute(sql, tuple(r))
                self.dbh.commit()
            except Exception as e:
                print(e)
        else:
            sql = "update memory set weight = weight + 1 where hash = %s"
            self.cur.execute(sql, (r[0], ))
            self.dbh.commit()

    def hashcheck(self, hash):
        sql = "select * from memory where hash = %s"
        self.cur.execute(sql, (hash, ))
        result = self.cur.fetchall()
        return len(result)

    def read_single(self, word, place):
        sql = "select * from memory where " + place + " = %s"
        self.cur.execute(sql, (word, ))
        result = self.cur.fetchall()
        return result

    def read_double(self, first, second):
        sql = "select * from memory where first = %s and second = %s"
        self.cur.execute(sql, (first, second))
        result = self.cur.fetchall()
        return result

    def read_double_back(self, second, third):
        sql = "select * from memory where third = %s and second = %s"
        self.cur.execute(sql, (third, second))
        result = self.cur.fetchall()
        return result