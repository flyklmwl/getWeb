from Config import config
from Tools import robot
from Tools import BackServer
import re

robot001 = robot.Robot('https://www.9moe.com/')
bs = BackServer.BackServer(config.GAL_URL, config.GAL_DB, config.GAL_TABLE)


def webpasre():
    print("开始解析网页")
#   r = requests.get(url='https://www.9moe.com/', headers=headers)  # 注意这个网页没有登录拿到的是缓存的页面，不是最新
    robot001.connectpage("https://www.9moe.com/")
    items = robot001.get_items('#alldiv .dcol .indexlbtit2')
    item_count = 0
    for item in items:
        item_count = item_count + 1

        if item_count == 11:
            break

        tz_link = "https://www.9moe.com/" + item.children().attr('href')
        result = robot001.connectpage(tz_link)
        hot_item = re.search('点击：(\d+|\-).*\|.*回复数：(\d+).*\|.*发表时间：(.*)&nbsp;\|', result.text)
        readid = re.findall('.*profile.php\?action=show.*\>(.*)\</a>', result.text)   # 楼主ID
        tui_item = robot001.get_item('#read_tui')
        type_item = robot001.get_item('div.drow:nth-child(4) > div:nth-child(2) > form:nth-child(2) > div:nth-child(5) '
                                      '> table:nth-child(1) > tr:nth-child(2) > td > a:nth-child(1)')

        tz = {
            'tz_title': item.find('.indexlbtit2_t').text(),
            'tz_link': tz_link,
            'tz_type': type_item.text(),
            'tz_dj': hot_item.group(1),
            'tz_hf': hot_item.group(2),
            'tz_c_time': hot_item.group(3),
            'tz_lz': readid[1],
            'tz_tui': tui_item.text()
        }
        # print(tz['tz_type'])
        if bs.add_save_data(tz, config.GAL_TABLE, 'tz_title'):   # 把字典存储到数据库，并把帖子标题和链接存到arr列表
            bs.packaging_mes(tz['tz_type'], tz['tz_title'], tz['tz_link'])
    bs.send_message(config.WX_CRT_GAL, config.WX_AGTID_GAL)


def main():
    print("现在开始!")
    islogintag = robot001.islogin()
    if islogintag is False:
        print(f"cookie失效，用户重新登录...")
        robot001.login("wind1314", "flyklmwl")
    webpasre()


if __name__ == '__main__':
    main()

