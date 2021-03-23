from Tools import robot, loggingset
from Tools import BackServer
from Config import config
import re
import json
import sys

bs = BackServer.BackServer(
        config.BOOK_URL,
        config.BOOK_DB,
        config.BOOK_TABLE,
        config.WX_CRT_GAL,
        config.WX_AGTID_GAL
)

bibi_movie_dict = {
    "0:名侦探柯南": "https://www.bilibili.com/bangumi/play/ss33378/",
    "1:黑色四叶草": "https://www.bilibili.com/bangumi/play/ss6422/"
}


def get_konan_date():
    robot001 = robot.Robot("www.baidu.com")
    result = robot001.connectpage("https://www.ytv.co.jp/conan/data/story.json")   # 这个只有1-960
    print(result.text)


def get_index(url):
    robot001 = robot.Robot("www.baidu.com")
    result = robot001.connectpage(url)
    jsonstr = re.search("\"epList\":(.*),\"epInfo\"", result.text)
    items = json.loads(jsonstr.group(1))
    i = 0
    for item in items:
        i += 1
        loggingset.logger.info(item["longTitle"])
        # print(i)
    # print(items)


def hint():
    loggingset.logger.info("列表参数不正确,请在biliplaybook后面输入数字对应的剧集!")
    for movie in bibi_movie_dict:
        loggingset.logger.info(movie)


if __name__ == '__main__':
    # get_konan_date()

    if len(sys.argv) < 2:
        print("请输入需要执行的参数： hnbook or biliplaybook")
    else:
        if sys.argv[1] == "hnbook":
            robot001 = robot.hn_book_Robot("www.baidu.com")
            book_dict = robot001.get_book_menu()
            bs.save_data(book_dict, "title")
            exit(0)
        if sys.argv[1] == "biliplaybook":
            if len(sys.argv) != 3:
                hint()
                exit(1)
            if sys.argv[2] == "0":
                get_index(bibi_movie_dict["0:名侦探柯南"])
                exit(0)
            if sys.argv[2] == "1":
                get_index(bibi_movie_dict["1:黑色四叶草"])
                exit(0)
            else:
                hint()
        else:
            loggingset.logger.error("参数不对!!!")
