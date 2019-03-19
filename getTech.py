from Config import config
from Tools import robot
from Tools import BackServer
from datetime import datetime


robot001 = robot.Robot("http://www.51cto.com/")
bs1 = BackServer.BackServer(
    config.TECH_URL,
    config.TECH_DB,
    config.TECH_TABLE,
    config.WX_CRT_TECH,
    config.WX_AGTID_TECH
)


def _51cto():
    robot001.connectpage("http://www.51cto.com/", 'gb2312')
    items = robot001.get_items('div.home-left-list:nth-child(7) > ul:nth-child(1) .rinfo > a:nth-child(1)')
    bs1.clear_arr()
    item_count = 0
    for item in items:
        item_count += 1
        if item_count == 11:
            break
        cto = {
            'title': item.text(),
            'link': item.attr('href'),
            'date': datetime.now()
        }
        if bs1.save_data(cto, 'link'):
            bs1.packaging_mes(cto['title'], cto['link'])
    bs1.send_message()


def segmentfault():
    robot001.connectpage("https://segmentfault.com/t/linux")
    items = robot001.get_items('.mr10')
    bs1.clear_arr()
    item_count = 0
    for item in items:
        item_count += 1
        if item_count <= 5:
            tiezi = {
                'title': item.text(),
                'link': 'https://segmentfault.com' + item.attr('href'),
                'date': datetime.now()
            }
            if bs1.save_data(tiezi, 'link'):
                bs1.packaging_mes(tiezi['title'], tiezi['link'])
    bs1.send_message()


def main():
    _51cto()
    segmentfault()


if __name__ == '__main__':
    main()
