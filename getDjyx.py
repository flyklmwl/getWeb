from Config import config
from Tools import robot, BackServer, loggingset


bs = BackServer.BackServer(
        config.DJYX_URL,
        config.DJYX_DB,
        config.DJYX_TABLE,
        config.WX_CRT_DJYX,
        config.WX_AGTID_DJYX
    )


@loggingset.logtrace
def main():
    loggingset.logger.info("----------开始抓取游戏评测数据----------")
    robot001 = robot.G3dmDJRobot("https://dl.3dmgame.com/")
    _3dm_news_data = robot001.parse()
    bs.save_data(_3dm_news_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------游戏评测数据已抓取完成----------")


if __name__ == "__main__":
    main()
