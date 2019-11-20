from socket import *
import sys
import time

class Client():
    def __init__(self,sockfd):
       self.sockfd=sockfd

    def do_regist(self):
        self.sockfd.send(b'1')
        data1=self.sockfd.recv(1024).decode()
        if data1=='ok':
            message=' '
            login_name=input("请输入注册名字：")
            login_password=input("请输入注册密码：")
            final_message=login_name+message+login_password
            self.sockfd.send(final_message.encode())
            data2=self.sockfd.recv(1024).decode()
            if data2=='ok':
                print("注册成功")
            else:
                print("注册失败，用户已存在")
        else:
            return

    def do_login(self):
        self.sockfd.send(b'2')
        data1 = self.sockfd.recv(1024).decode()
        if data1=='ok':
            message = ' '
            login_name = input("请输入登录名字：")
            login_password = input("请输入登录密码：")
            final_message = login_name + message + login_password
            self.sockfd.send(final_message.encode())
            data2 = self.sockfd.recv(1024).decode()
            if data2=='ok':
                print("登录成功")
            else:
                print("用户名或密码错误")
                return
            time.sleep(1)
            while True:
                print("----欢迎-----")
                print('1.查看单词')
                print('2.查看单词记录')
                print('3.退出')
                message=input('请选择:')
                if message == '1':
                    self.do_check(login_name)
                elif message == '2':
                    self.do_hist(login_name)
                elif message == '3':
                    sys.exit("谢谢使用！")
        else:
            return

    def do_check(self,login_name):
        self.sockfd.send(b'3')
        data1 = self.sockfd.recv(1024).decode()
        if data1 == 'ok':
            word = input("请输入单词：")
            message=login_name+' '+word
            self.sockfd.send(message.encode())
            data2 = self.sockfd.recv(1024).decode()
            print(data2)
        else:
            return

    def do_hist(self, login_name):
        self.sockfd.send(b'4')
        data1 = self.sockfd.recv(1024).decode()
        if data1 == 'ok':
            self.sockfd.send(login_name.encode())
            data2 = self.sockfd.recv(1024).decode()
            list=data2.split("#")
            for l in list:
                print(l)
        else:
            return

def main():
    sockfd = socket()
    sockfd.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    sockfd.connect(("127.0.0.1", 8888))
    client=Client(sockfd)
    while True:
        print("----欢迎-----")
        print('1.注册')
        print('2.登录')
        print('3.退出')
        message=input("请选择：")
        if message=='1':
           client.do_regist()
        elif message=='2':
           client.do_login()
        elif message=='3':
           sys.exit("谢谢使用！")
        else:
           print("指令有误，请重新输入")
           continue



if __name__ == '__main__':
    main()