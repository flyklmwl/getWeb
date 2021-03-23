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
        883968, 168243072, 80467330, 359439463, 15773384, 396692077, 16682415, 131494610, 207539637, 928123, 71302461
    ]

    bdquene = [
        282994, 11073, 345630501, 3046429, 415479453, 79577853, 596324576, 375375, 176037767, 450595813, 4162287,
        604003146, 6574487, 483879799, 590490400, 26139491, 369750017, 4474705, 2920960, 777536, 433351, 326246517,
        62540916, 562197, 416128940, 35359510, 147166910, 26240675, 37663924, 946974, 16539048, 13354765, 10119428,
        5970160, 470156882, 168598, 94281836, 452309333, 96070394, 7788379, 3066511, 1958342, 39627524, 23604445,
        515993, 454719565, 5293668, 730732, 59905809, 414641554, 7487399, 27756469, 927587, 1577804, 18202105,
        517327498, 51896064, 79061224, 14110780, 519872016, 19642758, 279583114, 163637592, 546195, 250111460, 3766866,
        279991456, 16794231, 43222001, 9824766, 25150941, 466272, 258150656, 2206456, 25422790, 1420982, 3353026,
        10874201, 436473455, 72270557, 63231, 29329085, 5294454, 285499073, 17819768, 99157282, 648113003, 2200736,
        378885845, 254463269, 113362335, 353539995, 122879, 7552204, 38351330, 21837784, 585267, 8366990, 116683,
        295723
    ]
    for mid in quene:
        get_bilibili_Data(str(mid))

    for mid in bdquene:
        get_bilibili_Data(str(mid))

    # robot1 = robot.BilibiliRobot("https://www.bilibili.com/activity/web/view/data/814?csrf=9ed488abc43c1d2721e7e99e8d70c2a5")
    # robot1.parsebd()
    # print(list(set(quene).difference(set(bdquene))))

    loggingset.logger.info("----------Bilibili数据已抓取完成----------")


if __name__ == "__main__":
    main()
