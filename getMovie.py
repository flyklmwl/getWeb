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

    loggingset.logger.info("----------电影数据已抓取完成----------")


if __name__ == "__main__":
    main()
