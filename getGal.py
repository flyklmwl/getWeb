from Config import config
from Tools import robot
from Tools import BackServer


def main():
    bs = BackServer.BackServer(
        config.GAL_URL,
        config.GAL_DB,
        config.GAL_TABLE,
        config.WX_CRT_GAL,
        config.WX_AGTID_GAL,
    )
    robot001 = robot.GalRobot("https://www.9moe.com/")

    islogintag = robot001.islogin()
    if islogintag is False:
        print(f"没有登陆网页，用户重新登录...")
        robot001.login("wind1314", "flyklmwl")

    gal_dict = robot001.parse()
    bs.save_update_data(gal_dict, "tz_link")
    bs.packaging_mes("tz_title", "tz_link")
    bs.send_message()


if __name__ == "__main__":
    main()
