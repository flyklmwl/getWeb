from pyquery import PyQuery as pq
import http.cookiejar as cookielib
import requests
import os


class Robot:
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}

    headers = {'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 '
                         '(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36'}
    open_session = requests.session()
    result = 'zero'

    def __init__(self, url):    # 传入解析地址
        self.url = url

    def islogin(self):
        self.open_session.cookies = cookielib.LWPCookieJar(filename=os.getcwd() + "/Log/galcookies.txt")
        try:
            self.open_session.cookies.load()
        except FileNotFoundError:
            print('没有cookie文件')
        try:
            responseres = self.open_session.get("https://www.9moe.com/kf_share.php?ti=cn", headers=self.headers,
                                                allow_redirects=False)
        except TimeoutError:
            print('没有登陆')
        print(f"isLogin = {responseres.status_code}")
        if responseres.status_code != 200:
            return False
        else:
            return True

    def login(self, username, password):
        print("正在登陆...")
        postdata = {
            "forward": '',
            "jumpurl": 'https://www.9moe.com/index.php',
            "step": '2',
            "lgt": '1',
            "hideid": '0',
            "cktime": '31536000',
            "pwuser": username,
            "pwpwd": password,
            "submit": '(unable to decode value)',
        }

        posturl = "https://www.9moe.com/login.php?"
        self.open_session.post(posturl, data=postdata, headers=self.headers, allow_redirects=False)  # 注意这里加了headers的话，后面的get方法也要加headers才能用登陆的身份拿到网页

        #   print(f"statusCode = {responseres.status_code}")       打印是否成功
        #   print(f"text = {responseres.text}")
        self.open_session.cookies.save()

    def connectpage(self, *url, **args):     # 定义两个参数 第一个为连接网址，第二个为编码, 第三个参数为cookie
        num = 3     # 重试次数
        while num > 0:
            try:
                self.result = self.open_session.get(url[0], **args)
            except requests.exceptions.ConnectTimeout:
                print('Timeout, try again')
                num -= 1
            except requests.exceptions.ReadTimeout:
                print('ReadTimeout,try again')
                num -= 1
            else:
                print('ok')  # 成功获取
                if len(url) > 1:
                    self.result.encoding = url[1]
                return self.result
        else:
            print('Try 3 times, But all failed')    # 3次都失败
            exit(-1)

    def get_item(self, select_css):
        doc = pq(self.result.text)
        item = doc(select_css)
        return item

    def get_items(self, select_css):
        doc = pq(self.result.text)
        item = doc(select_css).items()
        return item

    # def parse_json(self, json, list):
    #     print(a)
    #     return True



