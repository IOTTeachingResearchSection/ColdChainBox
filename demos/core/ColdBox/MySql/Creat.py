import pymysql
from itertools import chain

#user='debian-sys-maint'
#password='VShIsIqvYFvcb5q1'

class CreatDataBase:
    def __init__(self,user,password) -> None:
        self.user = user
        self.password = password
        self.mydb = pymysql.connect(
            host="localhost", 
            port=3306,
            user=self.user, 
            password=self.password,
            charset='utf8mb4' 
            )
        self.mycursor = self.mydb.cursor()

    def creat(self,dbname='coldboxtest'):
        sql = 'CREATE DATABASE IF NOT EXISTS ' + str(dbname)
        self.mycursor.execute(sql)

    def close(self):
        self.mycursor.close()
        self.mydb.close()


class CreatTable:
    def __init__(self,user,password,database='coldboxtest') -> None:
        self.user = user
        self.password = password
        self.database = database
        self.mydb = pymysql.connect(
            host="localhost", 
            port=3306,
            user=self.user, 
            password=self.password,
            database=self.database,
            charset='utf8mb4' 
            )
        self.mycursor = self.mydb.cursor()

    def creat(self):
        tableName = 'rootuser'
        sql = 'create table ' + tableName + '(username varchar(20) not null, password varchar(20) not null, primary key(username))'
        self.mycursor.execute(sql)

        tableName = 'food'
        sql = 'create table ' + tableName + '(id varchar(20) not null , foodname varchar(10) not null, putpeopleid varchar(20), putpeople varchar(10), puttime varchar(50), getpeopleid varchar(20), getpeople varchar(10), gettime varchar(50), faceurl varchar(300), maskurl varchar(300), handsurl varchar(300), primary key(id))'
        self.mycursor.execute(sql)
        
    def close(self):
        self.mycursor.close()
        self.mydb.close()


# if __name__ == '__main__':
#     user='debian-sys-maint'
#     password='VShIsIqvYFvcb5q1'
#     dbname = 'rootuser'
#     cdb = CreatDataBase(user,password)
#     cdb.creat()
#     ct = CreatTable(user,password)
#     ct.creat()

    # conn = pymysql.connect(host='localhost', user='root', password='888888', charset='utf8mb4', database='coldboxtest')
    # cursor = conn.cursor()
    # sql = "insert into food (putpeople, puttime, getpeople, gettime, faceurl, maskurl, handsurl) values (value1, value2, value3, value4, value5, value6, value7)"
    # cursor.execute(sql)

    # sql_2 = "select * from food"
    # cursor.execute(sql_2)
    # data = cursor.fetchall()
    # resultlist = list(chain.from_iterable(data))




if __name__ == '__main__':
    user='debian-sys-maint'
    password='VShIsIqvYFvcb5q1'
    dbname = 'rootuser'
    # cdb = CreatDataBase(user,password)
    # cdb.creat()
    ct = CreatTable(user,password)
    ct.creat()