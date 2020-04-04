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
    if action == 'previous':
        ActionKey(37)
    CtrlAltKeyUp()

def NetControl():
    try:
        WebPort = int(input('Input server port,default [10086]:'))
    except Exception:
        WebPort = 10086
    #WebAddr = tuple('192.168.1.5')
    WebHost = ('0.0.0.0', WebPort)
    WebRespHeader = '''HTTP/1.1 200 OK
Content-Type: text/html

'''.encode(encoding='utf-8')
    #建立新socket
    sck = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    #绑定端口和监听
    sck.bind(WebHost)
    sck.listen(100)
    #报头报文分隔符
    LineSeparator = '\r\n\r\n'
    print('Web Port %d' %WebPort)
    print('URL: http://192.168.1.5:%d' %WebPort)

    while True:
        client, address = sck.accept()
        request = client.recv(1024).decode(encoding='utf-8')
        request_text = request.split(LineSeparator)
        request_header = request_text[0]
        request_body = request_text[1]
        request_method = request_header.split(' ')[0]
        request_url = request_header.split(' ')[1]
        
        WebRespBody = '''<!DOCTYPE html>
        <html>
            <form action="/" method="post" style="text-align:center">
                <p>Pause: <input type="text" name="act" value="pause"/></p>
                <input type="submit" value="pause" />
            </form>
            <form action="/" method="post" style="text-align:center">
                <p>Next: <input type="text" name="act" value="next"/></p>
                <input type="submit" value="next" />
            </form>
            <form action="/" method="post" style="text-align:center">
                <p>Previous: <input type="text" name="act" value="previous"/></p>
                <input type="submit" value="previous" />
            </form>
        </html>'''.encode(encoding='utf-8')
        WebResp = ''.encode(encoding='utf-8')
        print(address)
        #print('RAW-BEGIN:\r\n' + request + '\r\nEND-RAW')
        print('RAW-HEADER:' + request_header + 'RAW-HEADER-END')
        #print('RAW-BODY:' + request_body + 'RAW-BODY-END')
        print('RAW-URL:' + request_url + 'RAW-URL-END')
        if request_method == 'GET':
            WebResp += WebRespHeader + WebRespBody
            client.sendall(WebResp)
        elif request_method == 'POST':
            print('POST')
            WebResp += WebRespHeader + WebRespBody
            print('RAW-BODY:' + request_body + 'RAW-BODY-END')

            if request_body == 'act=pause':
                MediaControl('pause')
            elif request_body == 'act=previous':
                MediaControl('previous')
            elif request_body == 'act=next':
                MediaControl('next')
            else:
                print('ERROR')
                
            client.sendall(WebResp)
        client.close()

if __name__=="__main__":
    NetControl()
    #MediaControl('pause')
