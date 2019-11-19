"""
mysql.py
pymysql 操作的流程演示
"""
import  pymysql

#  链接数据库
db = pymysql.connect(host='localhost',
                     port=3306,
                     user='root',
                     password='123456',
                     database='stu',
                     charset='utf8')

# 生成游标对象 (用于操作数据库数据，获取sql执行结果的对象)
cur = db.cursor()

# 执行各种数据库sql操作
cur.execute("de132115345634563464354321lete from cls1 where name='Tom';")
db.commit()

# 关闭游标和数据库链接
cur.close()
db.close()






