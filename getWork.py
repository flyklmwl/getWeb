from Config import config
from Tools import robot, BackServer, loggingset


@loggingset.logtrace
def main():
    bs = BackServer.BackServer(
        config.WORK_URL,
        config.WORK_DB,
        config.WORK_TABLE,
        config.WX_CRT_WORK,
        config.WX_AGTID_WORK,
    )

    loggingset.logger.info("----------开始抓取工作数据----------")
    robot001 = robot.LagouRobot("https://www.lagou.com/jobs/list_运维")
    lagou_data = robot001.parse()
    bs.save_data(lagou_data, "link")
    bs.packaging_mes("jobName", "updateDate", "salary", "companyName", "link")
    bs.send_message()
    loggingset.logger.info("----------工作数据已抓取完成----------")


if __name__ == "__main__":
    main()
