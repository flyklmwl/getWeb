from Config import config
from Tools import robot
from Tools import BackServer


def main():
    bs = BackServer.BackServer(
        config.HOUSE_URL,
        config.HOUSE_DB,
        config.HOUSE_TABLE,
        config.WX_CRT_HOUSE,
        config.WX_AGTID_HOUSE,
    )

    robot001 = robot.AnjkRobot("https://cs.fang.anjuke.com/loupan/")
    anjk_data = robot001.parse()
    bs.save_data(anjk_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()


if __name__ == "__main__":
    main()
