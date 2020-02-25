from Config import config
from Tools import robot
from Tools import BackServer


def main():
    bs = BackServer.BackServer(
        config.WORK_URL,
        config.WORK_DB,
        config.WORK_TABLE,
        config.WX_CRT_WORK,
        config.WX_AGTID_WORK,
    )
    robot001 = robot.LagouRobot("https://www.lagou.com/jobs/list_运维")
    lagou_data = robot001.parse()
    bs.save_data(lagou_data, "link")
    bs.packaging_mes("jobName", "updateDate", "salary", "companyName", "link")
    bs.send_message()


if __name__ == "__main__":
    main()
