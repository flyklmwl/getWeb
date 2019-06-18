from Config import config
from Tools import robot
from Tools import BackServer
from pyquery import PyQuery as pq
from Tools import parse_bilibili as pb
import pysnooper

robot001 = robot.Robot("http://www.baidu.com")
bs1 = BackServer.BackServer(
    config.MOVIE_URL,
    config.MOVIE_DB,
    config.MOVIE_TABLE,
    config.WX_CRT_MOVIE,
    config.WX_AGTID_MOVIE,
)


@pysnooper.snoop()
def parse_maoyan():
    robot001.connectpage("https://maoyan.com/", headers=config.headers)

    items = robot001.get_items(".ranking-box a")
    item_count = 0
    for item in items:
        print(item)
        item_count = item_count + 1
        doc = pq(item)
        if item_count == 1:
            name = doc(".ranking-top-moive-name").text()
        else:
            name = doc(".ranking-movie-name").text()
        movie = {"title": name, "link": "https://www.maoyan.com" + item.attr("href"), "type": "maoyan"}
        if bs1.save_data(movie, "link"):
            bs1.packaging_mes(movie["title"], movie["link"])
    bs1.send_message()


def main():
    parse_maoyan()
    pb.parse_bilibili(robot001, bs1, "927587", "15773384", "17819768", "883968")


if __name__ == "__main__":
    main()
