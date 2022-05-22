import pymysql

class DataHandle: 
    
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

    def upload(self,**data):
        key = ''
        values = ''
        for k,v in data.items():
            key = key + ',' + k
            values = values + ',\'' + v + '\''
        sql = "insert into food(%s) values (%s)"%(key[1:],values[1:])
        print(sql)
        self.mycursor.execute(sql)

if __name__ == '__main__':
    user = 'debian-sys-maint'
    password = 'VShIsIqvYFvcb5q1'
    a = DataHandle(user,password)
    a.upload(id='20220504001',foodname='西红柿')