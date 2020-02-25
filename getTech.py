from Config import config
from Tools import robot
from Tools import BackServer
from Tools import parse_bilibili as pb


def main():
    bs = BackServer.BackServer(
        config.TECH_URL,
        config.TECH_DB,
        config.TECH_TABLE,
        config.WX_CRT_TECH,
        config.WX_AGTID_TECH,
    )

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

    robot003 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=16682415&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot003.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot004 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=396692077&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot004.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot005 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=168243072&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot005.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot006 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=131494610&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot006.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot007 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=359439463&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot007.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot008 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=71302461&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot008.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()

    robot009 = robot.BilibiliRobot("https://api.bilibili.com/x/space/arc/search?mid=80467330&pn=1&ps=25&jsonp=jsonp")
    bilibili_data = robot009.parse()
    bs.save_data(bilibili_data, "link")
    bs.packaging_mes("title", "link")
    bs.send_message()


if __name__ == "__main__":
    main()
