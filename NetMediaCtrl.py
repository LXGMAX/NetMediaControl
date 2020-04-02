'''
Environmental requirements: python3 pypiwin32
'''
import sys
import win32api
import win32con
import socket

def CtrlAltKeyDown():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(18, 0, 0, 0)  # alt键位码是18
    
def CtrlAltKeyUp():
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    
# p键位码是80,right键位码是39,left键位码是37,D键位码是68
def ActionKey(KCode):
    win32api.keybd_event(KCode, 0, 0, 0)  
    win32api.keybd_event(KCode, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    
def MediaControl(action):
    CtrlAltKeyDown()    
    if action == 'pause':
        ActionKey(80)
    if action == 'next':
        ActionKey(39)
    if action == 'Previous':
        ActionKey(37)
    CtrlAltKeyUp()

def NetControl():
    print("MCServer Starting")
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    sock.bind(('127.0.0.1', 10086))  #配置soket，绑定IP地址和端口号
    sock.listen(5) #设置最大允许连接数，各连接和server的通信遵循FIFO原则
    print("MCServer is listenting port 10086,max connection 5")
    http_resp = """\
HTTP/1.1 200 OK

Web Page
"""
    while True:
        client_cnt,client_addr = sock.accept()
        try:
            connection.settimeout(50)
            rqst = sock.recv(1024)
            print(rqst.decode("utf-8"))
            client_cnt.sendall(http_resp.encode("utf-8"))
            print(rqst,client_addr)
            
        except:
            print("socket ERROR")
            sock.close()
            break
    sock.close()    
if __name__=="__main__":
    NetControl()
    MediaControl('next')
