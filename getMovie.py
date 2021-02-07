from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.MOVIE_URL,
        config.MOVIE_DB,
        config.MOVIE_TABLE,
        config.WX_CRT_MOVIE,
        config.WX_AGTID_MOVIE,
    )

    loggingset.logger.info("----------开始抓取电影数据----------")
    robot001 = robot.MaoYanRobot("https://maoyan.com/")
    maoyan_data = robot001.parse()
    bs.save_data(maoyan_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot002 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=927587&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot002.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot003 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=15773384&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot003.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot004 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=17819768&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot004.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot005 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=883968&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot005.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot006 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=928123&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot006.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "author", "date", "link")
    bs.send_message()

    robot007 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=207539637&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot007.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "author", "date", "link")
    bs.send_message()
    loggingset.logger.info("----------电影数据已抓取完成----------")


if __name__ == "__main__":
    main()
