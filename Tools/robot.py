from pyquery import PyQuery as pq
from Tools import BackServer
from Config import config
from datetime import datetime
import http.cookiejar as cookielib
from dateutil.parser import parse
import requests
import os
import re
import time

import parsel


bs = BackServer.BackServer(
    config.GAL_URL,
    config.GAL_DB,
    config.GAL_TABLE,
    config.WX_CRT_GAL,
    config.WX_AGTID_GAL,
)


class Robot:
    # headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:63.0) Gecko/20100101 Firefox/63.0'}

    headers = {
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 "
        "(KHTML, like Gecko) Chrome/70.0.3538.110 Safari/537.36"
    }
    open_session = requests.session()
    result = "zero"

    def __init__(self, url):  # 传入解析地址
        self.url = url

    def connectpage(self, *url, **args):  # 定义两个参数 第一个为连接网址，第二个为编码, 第三个参数为cookie
        num = 3  # 重试次数
        while num > 0:
            try:
                self.result = self.open_session.get(url[0], **args)
            except requests.exceptions.ConnectTimeout:
                print("Timeout, try again")
                num -= 1
            except requests.exceptions.ReadTimeout:
                print("ReadTimeout,try again")
                num -= 1
            else:
                print("已成功获取网页")  # 成功获取
                if len(url) > 1:
                    self.result.encoding = url[1]
                return self.result
        else:
            print("Try 3 times, But all failed")  # 3次都失败
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


class GalRobot(Robot):
    def parse(self):
        print("这里是解析的具体方法")
        print("开始解析网页")
        #   r = requests.get(url='https://www.9moe.com/', headers=headers)  # 注意这个网页没有登录拿到的是缓存的页面，不是最新
        self.connectpage(self.url, headers=config.headers, timeout=5)

        items = self.get_items("#alldiv .dcol .indexlbtit2")
        item_count = 0
        data_list = []

        for item in items:
            item_count = item_count + 1

            if item_count == 11:
                break

            # 获取帖子标题、链接、类型
            tz_title = item.find(".indexlbtit2_t").text()
            tz_link = "https://www.9moe.com/" + item.children().attr("href")

            result = self.connectpage(tz_link, headers=config.headers, timeout=5)
            tz_type = self.get_item(
                "div.drow:nth-child(3) > div:nth-child(1) > form:nth-child(2) > div:nth-child(5)"
                " > table:nth-child(1) > tr:nth-child(2) > td:nth-child(1) > a:nth-child(1)").text()
            # 获取帖子的点击数、回复数、创建时间
            get_item = re.search(
                "点击：(\d+|\-).*\|.*回复数：(\d+).*\|.*发表时间：(.*)&nbsp;\|", result.text
            )
            if get_item.group(1) is "-":
                tz_dj = 0
            else:
                tz_dj = int(get_item.group(1))
            tz_c_time = datetime.strptime(
                get_item.group(3)[:-1] + ":00", "%Y-%m-%d %H:%M:%S"
            )
            tz_hf = int(get_item.group(2))

            # 获取作者id,推荐数量
            readid = re.findall(
                ".*profile.php\?action=show.*\>(.*)\</a>", result.text
            )  # 楼主ID
            tz_tui = int(self.get_item("#read_tui").text()[3:])

            tz = {
                "tz_title": tz_title,
                "tz_link": tz_link,
                "tz_type": tz_type,
                "tz_dj": tz_dj,
                "tz_hf": tz_hf,
                "tz_c_time": tz_c_time,
                "tz_lz": readid[1],
                "tz_tui": tz_tui,
            }
            data_list.append(tz)
        return data_list

    def islogin(self):
        self.open_session.cookies = cookielib.LWPCookieJar(
            filename=os.getcwd() + "/Log/galcookies.txt"
        )
        try:
            self.open_session.cookies.load()
        except FileNotFoundError:
            print("没有cookie文件")
        try:
            responseres = self.open_session.get(
                "https://www.9moe.com/index.php",
                headers=self.headers,
                allow_redirects=False,
            )
        except TimeoutError:
            print("没有登陆")
        # print(f"isLogin = {responseres.status_code}")
        print("获取首页代码")
        # print(responseres.text)
        result = re.search("wind1314", responseres.text, re.M)
        if result:
            print("已经登陆")
            return True
        else:
            return False

    def login(self, username, password):
        self.open_session.cookies = cookielib.LWPCookieJar(
            filename=os.getcwd() + "/Log/galcookies.txt"
        )
        print("正在登陆...")
        postdata = {
            "forward": "",
            "jumpurl": "https://www.9moe.com/index.php",
            "step": "2",
            "lgt": "1",
            "hideid": "0",
            "cktime": "31536000",
            "pwuser": username,
            "pwpwd": password,
            "submit": "(unable to decode value)",
            # "submit": "%B5%C7%C2%BC"
        }

        posturl = "https://www.9moe.com/login.php?"
        self.open_session.post(
            posturl, data=postdata, headers=config.headers, allow_redirects=False
        )  # 注意这里加了headers的话，后面的get方法也要加headers才能用登陆的身份拿到网页

        #   print(f"statusCode = {responseres.status_code}")       打印是否成功
        #   print(f"text = {responseres.text}")
        self.open_session.cookies.save()


class YouXiaRobot(Robot):
    def parse(self):
        self.connectpage(self.url, "utf-8")
        get_date = re.search(".*时间：(.*)", self.get_item(".one_l_con_tag").text())
        data_list = []
        data = {
            "title": self.get_item(
                "body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) "
                "> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a"
            ).text(),
            "link": self.get_item(
                "body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) "
                "> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a"
            ).attr("href"),
            "date": datetime.strptime(get_date.group(1), "%Y-%m-%d"),
            "score": self.get_item(
                "body > div.npc_a > div.npc_t3 > div.t3_l "
                "> div:nth-child(1) > div.t3_l_one_r > div > span"
            ).text(),
            "type": 'youxia'
        }
        data_list.append(data)
        return data_list


class G3dmRobot(Robot):
    def parse(self):
        self.connectpage(self.url)
        data_list = []
        data = {
            "title": self.get_item(
                "body > div.content.clear > div.Content_L "
                "> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a"
            ).text(),
            "link": self.get_item(
                "body > div.content.clear > div.Content_L "
                "> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a"
            ).attr("href"),
            "date": datetime.strptime(self.get_item(".time").text()[:10], "%Y-%m-%d"),
            "score": self.get_item(
                "body > div.content.clear > div.Content_L "
                "> div.yc_warp_list > ul > li:nth-child(1) > div.net > div > div.p > a"
            ).text(),
            "type": "3dm"
        }
        data_list.append(data)
        return data_list


class YmxkRobot(Robot):
    def parse(self):
        self.connectpage(self.url, "utf-8")
        data_list = []
        data = {
            "title": self.get_item(
                "body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block "
                "> ul > li:nth-child(1) > div.con > div.tit > a"
            ).text(),
            "link": self.get_item(
                "body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul "
                "> li:nth-child(1) > div.con > div.tit > a"
            ).attr("href"),
            "date": datetime.strptime(self.get_item(".time").text()[:10], "%Y-%m-%d"),
            "score": self.get_item(
                "body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul "
                "> li:nth-child(1) > div.pc > div"
            ).text(),
            "type": "ymxk"
        }
        data_list.append(data)
        return data_list


class G17173Robot(Robot):
    def parse(self):
        self.connectpage(self.url)
        get_date = re.search(".*发表时间：(.*)", self.get_item(".date").text()[:15])
        data_list = []
        data = {
            "title": self.get_item(
                "#content > div.page-swsearch-main.search-mod > div.main > div.result-mod "
                "> div > ul > li:nth-child(1) > div.text > h3 > a"
            ).text(),
            "link": self.get_item(
                "#content > div.page-swsearch-main.search-mod > div.main > div.result-mod "
                "> div > ul > li:nth-child(1) > div.text > h3 > a"
            ).attr("href"),
            "date": datetime.strptime(get_date.group(1), "%Y-%m-%d"),
            "score": "没有......",
            "type": "17173"
        }
        data_list.append(data)
        return data_list


class G3dmDJRobot(Robot):
    def parse(self):
        self.connectpage(self.url)
        items = self.get_items("html body div.content div.listwrap ul.downllis li div.item")
        data_list = []
        for item in items:
            data = {
                "title": item(".bt a").text(),
                "link": item(".bt a").attr("href"),
                "date": parse(item("ol:nth-child(2) > li:nth-child(5) > i:nth-child(1)").text()),
                "type": "3dm_dj"
            }
            data_list.append(data)
            print(data["date"])
        return data_list


class JsonRobot(Robot):
    def __init__(self, url, datadict):
        super().__init__(url)
        self.datadict = datadict

    def parse(self):
        result = self.connectpage(self.url)
        appid = result.json()
        data_list = []
        for app in appid:
            singledict = {}
            for key in self.datadict:
                try:
                    singledict[key] = app[self.datadict[key]]
                except KeyError as e:
                    print("该变量没有找到相关字段：" + str(e))
                    singledict[key] = self.datadict[key]
            data_list.append(singledict)
        return data_list


class AnjkRobot(Robot):
    def parse(self):
        self.connectpage(self.url)
        data_list = []
        items = self.get_items("div.item-mod > div.infos")
        item_count = 0
        for item in items:
            item_count = item_count + 1
            if item_count > 10:
                break
            data = {
                "title": item("a.lp-name > h3 > span").text(),
                "link": item("a.lp-name").attr("href"),
                "locate": item(".address > span").text(),
                "huxing": item(".huxing > span").text()
            }
            data_list.append(data)
        return data_list


class MaoYanRobot(Robot):
    def parse(self):
        self.connectpage(self.url, headers=self.headers)
        items = self.get_items(".ranking-box a")
        data_list = []
        item_count = 0
        for item in items:
            item_count = item_count + 1
            doc = pq(item)
            if item_count == 1:
                name = doc(".ranking-top-moive-name").text()
            else:
                name = doc(".ranking-movie-name").text()
            data = {"title": name, "link": "https://www.maoyan.com" + item.attr("href"), "type": "maoyan"}
            data_list.append(data)
        return data_list


class ToutiaoRobot(Robot):
    def parse(self):
        result = self.connectpage(self.url, "utf-8")
        data_list = []
        news = result.json()["data"]
        for i in range(0, 10):
            data = {
                "title": news[i]["title"],
                "link": "https://www.toutiao.com" + news[i]["open_url"],
                "type": "今日头条",
                "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            }
            data_list.append(data)
        return data_list


class SinaSportRobot(Robot):
    def parse(self):
        self.result = self.connectpage(self.url, "utf-8")
        data_list = []
        items = self.get_items(".layout_sports_350_650 > div:nth-child(1) h3 a")
        for item in items:
            data = {
                "title": item.text(),
                "link": item.attr("href"),
                "type": "新浪体育",
                "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            }
            data_list.append(data)
        return data_list


class WeiBoRobot(Robot):
    def parse(self):
        self.result = self.connectpage(self.url)
        data_list = []
        items = self.get_items(
            "#pl_top_realtimehot > table:nth-child(1) > tbody:nth-child(2) a"
        )
        item_count = 0
        for item in items:
            item_count += 1
            if item_count == 10:
                break
            data = {
                "title": item.text(),
                "link": "https://s.weibo.com" + item.attr("href"),
                "type": "微博",
                "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            }
            data_list.append(data)
        return data_list


class ZhiHuRobot(Robot):
    def parse(self):
        result = self.connectpage(self.url, "gbk2312", headers=config.headers)
        data_list = []
        appid = result.json()["data"]
        for i in range(0, 10):
            data = {
                "hot": appid[i]["detail_text"],
                "title": appid[i]["target"]["title"],
                "link": "https://www.zhihu.com/question/" + str(appid[i]["target"]["id"]),
                "type": "知乎",
                "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            }
            data_list.append(data)
        return data_list


class TieBaRobot(Robot):
    def parse(self):
        result = self.connectpage(self.url, headers=config.headers)
        data_list = []
        print(result.text)
        baidu_tz = result.json()["data"]["bang_topic"]["topic_list"]
        for i in range(0, 10):
            data = {
                "title": baidu_tz[i]["topic_name"],
                "link": baidu_tz[i]["topic_url"],
                "type": "tieba",
                "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
            }
            data_list.append(data)
        return data_list


class TieBa2Robot(Robot):
    def __init__(self, url, author):
        super(TieBa2Robot, self).__init__(url)
        self.author = author

    def parse(self):
        # TODO 这里如果使用 headers=config.headers 的话，得到的网页源代码和实际不同，导致titile_url 为空

        self.connectpage(self.url)
        data_list = []
        page_source = parsel.Selector(self.result.text)
        title_url = page_source.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@href').extract()
        title_name = page_source.xpath('//div[@class="threadlist_lz clearfix"]/div/a/@title').extract()

        if len(title_url) == len(title_name):
            for i in range(len(title_url)):
                tieba = {
                    'link': "https://tieba.baidu.com" + title_url[i],
                    'title': title_name[i],
                    "type": "tieba",
                    "author": self.author,
                    "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S")
                }
                print(tieba)
                data_list.append(tieba)
        return data_list


class G3dmNewsRobot(Robot):
    def parse(self):
        self.connectpage(self.url, 'utf-8')
        data_list = []
        items = self.get_items(".Listwrap > div:nth-child(1) > ul li")
        for item in items:
            data = {
                "title": item("a").text(),
                "link": item("a").attr("href"),
                "date": parse((item("span").text())),
                "type": "3dm"
            }
            data_list.append(data)
        return data_list


class T51CtoRobot(Robot):
    def parse(self):
        self.connectpage(self.url, "gb2312")
        data_list = []
        items = self.get_items(
            "div.home-left-list:nth-child(7) > ul:nth-child(1) .rinfo > a:nth-child(1)"
        )
        item_count = 0
        for item in items:
            item_count += 1
            if item_count == 11:
                break
            data = {
                   "title": item.text(),
                   "link": item.attr("href"),
                   "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S"),
                   "type": "51cto"}
            data_list.append(data)
        return data_list


class SegmentFaultRobot(Robot):
    def parse(self):
        self.connectpage(self.url)
        data_list = []
        items = self.get_items(".mr10")
        item_count = 0
        for item in items:
            item_count += 1
            if item_count <= 5:
                data = {
                    "title": item.text(),
                    "link": "https://segmentfault.com" + item.attr("href"),
                    "date": datetime.strptime(time.strftime('%Y-%m-%d %H:%M:%S'), "%Y-%m-%d %H:%M:%S"),
                    "type": "segmentfault"
                }
                data_list.append(data)
        return data_list


class LagouRobot(Robot):
    def parse(self):
        self.connectpage(self.url, headers=config.headers_lagou, timeout=5)
        data_list = []
        para = {"city": "长沙", "needAddtionalResult": "false"}
        # if len(args) == 1:
        #     para = {"city": args[0], "needAddtionalResult": "false"}
        # else:
        #     para = {"city": args[0], "needAddtionalResult": "false", "kd": args[1]}

        result = self.connectpage("https://www.lagou.com/jobs/positionAjax.json", "utf-8", params=para, headers=config.headers_lagou, timeout=5)
        appid = result.json()["content"]["positionResult"]["result"]
        for i in range(0, 10):
            data = {
                "jobName": appid[i]["positionName"],
                "updateDate": datetime.strptime(
                    appid[i]["createTime"], "%Y-%m-%d %H:%M:%S"
                ),
                "id": appid[i]["positionId"],
                "salary": appid[i]["salary"],
                "companyName": appid[i]["companyFullName"],
                "link": "https://www.lagou.com/jobs/"
                        + str(appid[i]["positionId"])
                        + ".html",
                "type": "lagou"
            }
            data_list.append(data)
        return data_list


class BilibiliRobot(Robot):
    def parse(self):
        data_list = []
        result = self.connectpage(self.url, config.headers)
        vlist = result.json()["data"]["list"]["vlist"]
        if vlist:
            for item in vlist:
                video = {
                    "title": item["title"],
                    "link": "https://www.bilibili.com/video/av" + str(item["aid"]),
                    "date": datetime.fromtimestamp(item["created"]),
                    "author": item["author"],
                    "type": "哔哩哔哩"
                }
                data_list.append(video)
            return data_list
