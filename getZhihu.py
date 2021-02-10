from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.NEWS_URL,
        config.NEWS_DB,
        config.NEWS_TABLE,
        config.WX_CRT_NEWS,
        config.WX_AGTID_NEWS,
    )

    loggingset.logger.info("----------开始抓取知乎数据----------")
    robot001 = robot.ZhiHuRobot("https://api.zhihu.com/topstory/hot-list?limit=10")
    zhihu_data = robot001.parse()
    bs.save_data(zhihu_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------知乎数据已抓取完成----------")


if __name__ == "__main__":
    main()