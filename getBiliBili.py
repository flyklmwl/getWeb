from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.BiliBili_URL,
        config.BiliBili_DB,
        config.BiliBili_TABLE,
        config.WX_CRT_BiliBili,
        config.WX_AGTID_BiliBili,
    )

    loggingset.logger.info("----------开始抓取Bilibili数据----------")

    def get_bilibili_Data(mid):
        robotx = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=" + mid  +"&pn=1&ps=25&jsonp=jsonp")
        bilibili_data = robotx.parse()
        bs.save_data(bilibili_data, "link")
        bs.packaging_mes("title", "link", "date", "author")
        bs.send_message()

    quene = [
        927587, 15773384, 17819768, 883968, 928123, 207539637, 16682415, 396692077, 168243072, 131494610,
        359439463, 71302461, 80467330
    ]

    for mid in quene:
        get_bilibili_Data(str(mid))

    loggingset.logger.info("----------Bilibili数据已抓取完成----------")


if __name__ == "__main__":
    main()
