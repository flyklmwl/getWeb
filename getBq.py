from Config import config
from Tools import robot
from Tools import BackServer
import requests
import time
from datetime import datetime


robot001 = robot.Robot("www.baidu.com")
bs1 = BackServer.BackServer(
    config.TECH_URL,
    config.TECH_DB,
    config.TECH_TABLE,
    config.WX_CRT_TECH,
    config.WX_AGTID_TECH,
)


def parse_bq(url):
    result = robot001.connectpage(url)
    # print(result.text)
    items = robot001.get_items(".tagbqppdiv")

    for item in items:
        # print(item)
        img_url = item("img").attr("data-original")
        hz = img_url[-4:]
        title = item("a").attr("title") + hz
        download(img_url, "img\\" + title)
        time.sleep(3)
        # print(title)


def download(url, path):
    r = requests.get(url)
    # print("ok")
    try:
        with open(path, "wb") as f:
            f.write(r.content)
        f.close()
    except OSError:
        print("有问题")


def main():
    for x in range(1, 10):
        parse_bq("https://www.fabiaoqing.com/biaoqing/lists/page/" + str(x) + ".html")


if __name__ == '__main__':
    main()
