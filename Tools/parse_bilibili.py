from Config import config
from datetime import datetime


def parse_bilibili(ob1, ob2, *gid):
    for aid in gid:
        result = ob1.connectpage("https://api.bilibili.com/x/space/arc/search?mid=" + aid + "&pn=1&ps=25&jsonp=jsonp", config.headers)
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


if __name__ == '__main__':
    parse_bilibili()


