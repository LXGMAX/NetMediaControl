'''
Environmental requirements: python3 pypiwin32 attrs
'''
from http.server import HTTPServer, BaseHTTPRequestHandler
from typing import Dict, Type
import socket

import win32api
import win32con
from attr import dataclass


def CtrlAltKeyDown():
    win32api.keybd_event(17, 0, 0, 0)  # ctrl键位码是17
    win32api.keybd_event(18, 0, 0, 0)  # alt键位码是18


def CtrlAltKeyUp():
    win32api.keybd_event(18, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键
    win32api.keybd_event(17, 0, win32con.KEYEVENTF_KEYUP, 0)  # 释放按键


# p键位码是80,right键位码是39,left键位码是37,D键位码是68,L是76
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
    if action == 'like':
        ActionKey(76)
    CtrlAltKeyUp()


@dataclass
class Response:
    code: int
    header: Dict[str, str]
    content: str


@dataclass
class Request:
    path: str
    data: str


class Page:
    def do_get(self, request: Request) -> Response:
        pass

    def do_post(self, request: Request) -> Response:
        pass


class HomePage(Page):
    def do_get(self, request: Request) -> Response:
        return HomePage._get_home_page()

    @staticmethod
    def _get_home_page():
        return Response(code=200, header={'Content-type': 'Content-Type: text/html;charset=UTF-8'},
                        content=open('home.html').read())

    def do_post(self, request: Request) -> Response:
        action = request.data
        if action == 'act=pause':
            MediaControl('pause')
        elif action == 'act=previous':
            MediaControl('previous')
        elif action == 'act=next':
            MediaControl('next')
        elif action == 'act=like':
            MediaControl('like')
        return HomePage._get_home_page()


router: Dict[str, Type[Page]] = {
    '/': HomePage
}


class WebCommandRequestHandler(BaseHTTPRequestHandler):

    def do_GET(self):
        if self.path not in router.keys():
            self.return_page_not_found()
            return
        res = router.get(self.path)().do_get(Request(path=self.path, data=''))
        self._send_response(res)

    def return_page_not_found(self):
        self.send_error(404, 'are you ok?')

    def _send_response(self, res: Response):
        self.send_response(res.code)
        for k, v in res.header.items():
            self.send_header(k, v)
        self.end_headers()
        self.wfile.write(res.content.encode(encoding='utf-8'))

    def do_POST(self):
        if self.path not in router.keys():
            self.return_page_not_found()
            return
        length = int(self.headers['content-length'])
        res = router.get(self.path)().do_post(Request(path=self.path, data=self.rfile.read(length).decode()))
        self._send_response(res)
        pass


def get_host_ip():
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(('8.8.8.8', 80))
        ip = s.getsockname()[0]
    finally:
        s.close()
    return ip


def NetControl():
    try:
        port = int(input('Input server port,default [10086]:'))
    except Exception:
        port = 10086
    web_host = ('0.0.0.0', port)
    server = HTTPServer(web_host, WebCommandRequestHandler)
    print("web server started, listening at: %s" % str(web_host))
    print("URL: http://%s:10086" % str(get_host_ip()))
    server.serve_forever()


if __name__ == "__main__":
    NetControl()
