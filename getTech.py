from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.TECH_URL,
        config.TECH_DB,
        config.TECH_TABLE,
        config.WX_CRT_TECH,
        config.WX_AGTID_TECH,
    )

    loggingset.logger.info("----------开始抓取技术数据----------")
    robot001 = robot.T51CtoRobot("http://www.51cto.com/")
    _51cto_data = robot001.parse()
    bs.save_data(_51cto_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot002 = robot.SegmentFaultRobot("https://segmentfault.com/t/linux")
    segmentfault_data = robot002.parse()
    bs.save_data(segmentfault_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()
    loggingset.logger.info("----------技术数据已抓取完成----------")


if __name__ == "__main__":
    main()
