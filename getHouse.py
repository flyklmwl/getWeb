from Config import config
from Tools import robot
from Tools import BackServer


robot001 = robot.Robot("http://www.baidu.com")
bs1 = BackServer.BackServer(
    config.HOUSE_URL,
    config.HOUSE_DB,
    config.HOUSE_TABLE,
    config.WX_CRT_HOUSE,
    config.WX_AGTID_HOUSE,
)


def fanchan():
    result = robot001.connectpage(
        "https://cs.fang.anjuke.com/loupan/",
        headers=config.headers,
    )
    # print(result.text)
    # item = robot001.get_item("div.item-mod > div.infos > a.lp-name")
    items = robot001.get_items("div.item-mod > div.infos")
    item_count = 0
    for item in items:
        item_count = item_count + 1
        if item_count > 10:
            break
        fanzi = {
            "title": item("a.lp-name > h3 > span").text(),
            "link": item("a.lp-name").attr("href"),
            "locate": item(".address > span").text(),
            "huxing": item(".huxing > span").text()
        }
        if bs1.save_update_data(fanzi, "link"):
                bs1.packaging_mes(fanzi["title"], fanzi["link"], fanzi["locate"])
    bs1.send_message()


def main():
    fanchan()


if __name__ == "__main__":
    main()
