import pymysql
import re
db=pymysql.connect(host='localhost',
                   port=3306,
                   user='root',
                   password='123456',
                   database='dict',
                   charset='utf8')

#生成游标对象（用于操作数据库数据，获取sql执行结果的对象）
cur=db.cursor()


file=open("dict.txt","r")
args_list=[]
content=file.readlines()
for line in content:
    tuple=re.findall(r"(\S+)\s+(.*)",line)[0]
    print(tuple)
    args_list.append(tuple)
file.close()
sql="insert into words (word,mean) values (%s,%s);"
try:
    cur.executemany(sql,args_list)
    db.commit()
except:
    db.rollback()