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

    loggingset.logger.info("----------开始抓取新闻数据----------")
    robot001 = robot.ToutiaoRobot("https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=news_hot&utm_source="
                                  "toutiao&widen=1&tadrequire=true")
    toutiao_data = robot001.parse()
    bs.save_data(toutiao_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot002 = robot.SinaSportRobot("http://sports.sina.com.cn/nba/")
    sinasport_data = robot002.parse()
    bs.save_data(sinasport_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot003 = robot.WeiBoRobot("https://s.weibo.com/top/summary")
    weibo_data = robot003.parse()
    bs.save_data(weibo_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot004 = robot.ZhiHuRobot("https://api.zhihu.com/topstory/hot-list?limit=10")
    zhihu_data = robot004.parse()
    bs.save_data(zhihu_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot005 = robot.TieBaRobot("http://tieba.baidu.com/hottopic/browse/topicList")
    tieba_data = robot005.parse()
    bs.save_data(tieba_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot006 = robot.G3dmNewsRobot("https://www.3dmgame.com/")
    g3dmdj_data = robot006.parse()
    bs.save_data(g3dmdj_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot007 = robot.TieBa2Robot("https://tieba.baidu.com/f?kw=%E7%BB%8F%E5%85%B8jrpg&fr=index", "经典jrpg")
    tieba_rpg_data = robot007.parse()
    bs.save_data(tieba_rpg_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    # robot008 = robot.TieBa2Robot("https://tieba.baidu.com/f?kw=%E7%94%B5%E8%84%91&fr=home", "电脑吧")
    # tieba_pc_data = robot008.parse()
    # bs.save_data(tieba_pc_data, "link")
    # bs.packaging_mes("title", "link")
    # bs.send_message()

    robot009 = robot.TieBa2Robot("https://tieba.baidu.com/f?kw=%E7%AC%91%E8%AF%9D", "笑话吧")
    tieba_haha_data = robot009.parse()
    bs.save_data(tieba_haha_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot010 = robot.PSNRobot("http://psnine.com/")
    psndata = robot010.parse()
    bs.save_data(psndata, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------新闻数据已抓取完成----------")


if __name__ == "__main__":
    main()
