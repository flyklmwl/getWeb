from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.GAMETEST_URL,
        config.GAMETEST_DB,
        config.GAMETEST_TABLE,
        config.WX_CRT_GT,
        config.WX_AGTID_GT,
    )

    loggingset.logger.info("----------开始抓取游戏评测数据----------")
    robot001 = robot.YouXiaRobot("http://www.ali213.net/news/pingce/")
    youxia_data = robot001.parse()
    bs.save_data(youxia_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot002 = robot.G3dmRobot("https://www.3dmgame.com/original_40_1/")
    threedm_data = robot002.parse()
    bs.save_data(threedm_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot003 = robot.YmxkRobot("https://www.gamersky.com/review/")
    ymxk_data = robot003.parse()
    bs.save_data(ymxk_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot004 = robot.G17173Robot("http://newgame.17173.com/game-demolist.html")
    _17173_data = robot004.parse()
    bs.save_data(_17173_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot005 = robot.G3dmDJRobot("https://dl.3dmgame.com/")
    _3dm_news_data = robot005.parse()
    bs.save_data(_3dm_news_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    data = {
        "title": "title",
        "link": "link",
        "date": "createtime",
        "score": "bak2",
        "type": "163game"
    }

    robot006 = robot.JsonRobot("https://cain-api.gameyw.netease.com"
                               "/cain/site/config?app=3&code=eval_new&start=0&size=20",
                               data
                               )
    _163_data = robot006.parse()
    bs.save_data(_163_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------游戏评测数据已抓取完成----------")


if __name__ == "__main__":
    main()
