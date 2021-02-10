from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.GAME_NEWS_URL,
        config.GAME_NEWS_DB,
        config.GAME_NEWS_TABLE,
        config.WX_CRT_GAME_NEWS,
        config.WX_AGTID_GAME_NEWS,
    )

    loggingset.logger.info("----------开始抓取游戏新闻数据----------")
    robot006 = robot.G3dmNewsRobot("https://www.3dmgame.com/")
    g3dmdj_data = robot006.parse()
    bs.save_data(g3dmdj_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot010 = robot.PSNRobot("http://psnine.com/")
    psndata = robot010.parse()
    bs.save_data(psndata, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------游戏新闻数据已抓取完成----------")


if __name__ == "__main__":
    main()