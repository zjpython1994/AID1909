from socket import *
import pymysql
from multiprocessing import process
import signal,os,sys

class Server():
    def __init__(self,connfd):
        self.connfd=connfd
        self.db = pymysql.connect(host='localhost',
                             port=3306,
                             user='root',
                             password='123456',
                             database='dict',
                             charset='utf8')
        self.cur = self.db.cursor()


    def do_regist(self):
        self.connfd.send(b'ok')
        data=self.connfd.recv(1024).decode()
        name=data.split(" ")[0]
        password=data.split(" ")[1]
        sql = "select name from user where name='%s';"%name
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            self.connfd.send(b'no')
        else:
            sql = "insert into user (name,password) values (%s,%s);"
            try:
                self.cur.execute(sql,[name,password])
                self.db.commit()
            except Exception as e:
                print(e)
                self.db.rollback()
            self.connfd.send(b'ok')


    def do_login(self):
        self.connfd.send(b'ok')
        data = self.connfd.recv(1024).decode()
        name = data.split(" ")[0]
        password = data.split(" ")[1]
        sql = "select name,password from user where name=%s and password=%s"
        self.cur.execute(sql,[name,password])
        result = self.cur.fetchone()
        if result:
            self.connfd.send(b'ok')
        else:
            self.connfd.send(b'no')

    def do_check(self):
        self.connfd.send(b'ok')
        data = self.connfd.recv(1024).decode()
        name = data.split(" ")[0]
        word = data.split(" ")[1]
        sql='insert into hist(name,word) values(%s,%s);'
        try:
            self.cur.execute(sql,[name,word])
            self.db.commit()
        except Exception as e:
            print(e)
            self.db.rollback()
        sql="select mean from words where word='%s';"%word
        self.cur.execute(sql)
        result = self.cur.fetchone()
        if result:
            self.connfd.send(result[0].encode())
        else:
            self.connfd.send('没有该单词，请重新选择'.encode())

    def do_hist(self):
        self.connfd.send(b'ok')
        name = self.connfd.recv(1024).decode()
        sql = "select word,time from hist where name='%s';" %name
        self.cur.execute(sql)
        result = self.cur.fetchall()
        message=''
        if result:
            for i in result:
                message+=i[0]+' '+str(i[1])+'#'
            print(message)
            self.connfd.send(message.encode())

        else:
            self.connfd.send(b'no')


def main():
    #创建套接字
    sockfd=socket()
    sockfd.setsockopt(SOL_SOCKET,SO_REUSEADDR,1)
    sockfd.bind(("127.0.0.1", 8888))
    sockfd.listen(3)

    # #处理僵尸进程
    # signal.signal(signal.SIGCHLD,signal.SIG_IGN)

    while True:
        try:
            connfd,addr=sockfd.accept()
            print("链接了",addr)
        except KeyboardInterrupt:
            sockfd.close()
            sys.exit('服务器退出')
        except Exception as e:
            print(e)
            continue
        server = Server(connfd)
        while True:
            data=connfd.recv(1024).decode()
            if data=='1':
                server.do_regist()
            elif data == '2':
                server.do_login()
            elif data == '3':
                server.do_check()
            elif data == '4':
                server.do_hist()
            else:
                print(1)
                connfd.close()
                break
        server.cur.close()
        server.db.close()


if __name__ == '__main__':
    main()