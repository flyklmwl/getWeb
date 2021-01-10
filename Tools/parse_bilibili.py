from Config import config
from datetime import datetime
from Tools import robot
import re
import json


def parse_bilibili(ob1, ob2, *gid):
    for aid in gid:
        result = ob1.connectpage("https://api.bilibili.com/x/space/arc/search?mid=" + aid + "&pn=1&ps=25&jsonp=jsonp", config.headers)
        # print(result.text)
        ob2.clear_arr()
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
                if ob2.save_data(video, "link"):
                    ob2.packaging_mes(video["title"], video["link"])
            ob2.send_message()
        else:
            print("没有抓取到数据")


# https://www.bilibili.com/bangumi/play/ss33378/  名侦探柯南
# https://www.bilibili.com/bangumi/play/ss6422/   黑色四叶草
def get_index():
    robot001 = robot.Robot("www.baidu.com")
    result = robot001.connectpage("https://www.bilibili.com/bangumi/play/ss6422/")
    # robot001.sourcepage()
    # item = re.findall("\"epList\"(.*)\],\"epInfo\"", result.text)
    jsonstr = re.search("\"epList\":(.*),\"epInfo\"", result.text)
    items = json.loads(jsonstr.group(1))
    # items = re.findall("titleFormat(.*),", item.text)
    # print(type(item.group(1)))
    i = 0
    for item in items:
        i += 1
        # print(item)
        # print(item["title"])
        print(item["longTitle"])
        # print(i)
    # print(items)


if __name__ == '__main__':
    get_index()
