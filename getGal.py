from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.GAL_URL,
        config.GAL_DB,
        config.GAL_TABLE,
        config.WX_CRT_GAL,
        config.WX_AGTID_GAL,
    )
    loggingset.logger.info("----------开始抓取Galgame 帖子----------")
    robot001 = robot.GalRobot("https://bbs.kforz.com/")

    islogintag = robot001.islogin()
    if islogintag is False:
        loggingset.logger.info(f"没有登陆网页，用户重新登录...")
        robot001.login("wind1314", "flyklmwl")

    gal_dict = robot001.parse()
    bs.save_update_data(gal_dict, "tz_link")
    bs.packaging_mes("tz_title", "tz_link")
    bs.send_message()
    loggingset.logger.info("----------Galgame 抓取完成----------")


if __name__ == "__main__":
    main()
