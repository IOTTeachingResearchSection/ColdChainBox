import pymysql

class MySql:
    def __init__(self) -> None:
        self.user = 'root'
        self.password = '123456'
        self.database = 'coldboxtest'
        self.mydb = pymysql.connect(
            host="localhost", 
            port=3306,
            user=self.user, 
            database = self.database,
            password=self.password,
            charset='utf8' 
            )
        self.mycursor = self.mydb.cursor()

    def query(self,id,tbname='food'):  #查询
        
        sql = 'select * from %s where id="%s"'%(tbname,id)
        self.mycursor.execute(sql)
        results = self.mycursor.fetchall()  #返回字段
        fields = [field[0] for field in self.mycursor.description] #字段名
        ans = [dict(zip(fields, result)) for result in results]  #字段名+字段组成一个字典

        return ans[0] if len(ans) == 1 else None

    def queryAll(self,tbname='user'):  #查询
        
        sql = 'select * from %s'%(tbname)
        self.mycursor.execute(sql)
        ans = self.mycursor.fetchall()  #返回字段
        list = []
        for i in ans:
            list.append(i[0])
        return list

    def insert(self,tbname='food',**data): #插入
        key = ''
        values = ''
        for k,v in data.items():
            key = key + ',' + k
            values = values + ',\'' + v + '\''
        sql = "insert into %s(%s) values (%s)"%(tbname,key[1:],values[1:])
        self.mycursor.execute(sql)
        self.mydb.commit()

    def updata(self,id,tbname='food',**data): #更新
        s = ''
        id = '\'%s\''%(id)
        for k,v in data.items():
            s += '%s=\'%s\','%(k,v)
        
        sql = 'update %s set %s where id=%s'%(tbname,s[:-1],id)
        self.mycursor.execute(sql)
        self.mydb.commit()
        

if __name__ == '__main__':
    a = MySql()
    # a.insert(id='20220515005',foodname='荔枝')
#     a.upload(id='20220515001',foodname='西瓜')
    c = a.queryAll('food')
    print(c)
#     a.updata('20220515001',puttime=8,gettime=2)
#     c = a.query('20220515001')
#     print(c)