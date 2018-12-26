from Config import config
from Tools import robot
from Tools import BackServer
import re
from urllib.parse import quote


robot001 = robot.Robot("http://www.baidu.com")
bs1 = BackServer.BackServer(config.NEWS_URL, config.NEWS_DB, config.NEWS_TABLE)


def parse_toutiao():
    result = robot001.connectpage("https://www.toutiao.com/2/wap/search/extra/"
                                  "hot_word_list/?from=toutiao_pc&is_new_ui=1")
    # print(result.text)
    bs1.clear_arr()
    news_item = re.findall('\\\\\"q\\\\\":\\\\\"(\w+)\\\\\"', result.text, re.S)
    for x in range(0, 9):
        print(news_item[x])
        news = {
            'title': news_item[x],
            'link': 'https://m.toutiao.com/search/?keyword=' + quote(news_item[x]) + '&from=gs_hotlist',
            'type': '今日头条'
        }
        if bs1.add_save_data(news, config.NEWS_TABLE, 'title'):
            bs1.packaging_mes(news['title'], news['link'])
    bs1.send_message(config.WX_CRT_NEWS, config.WX_AGTID_NEWS)


def parse_sport():
    robot001.connectpage("http://sports.sina.com.cn/nba/", 'utf-8')
    news_items1 = robot001.get_items(".layout_sports_350_650 > div:nth-child(1) h3 a")
    print(news_items1)

    bs1.clear_arr()
    for item in news_items1:
        news = {
            'title': item.text(),
            'link': item.attr('href'),
            'type': '新浪体育'
        }
        if bs1.add_save_data(news, config.NEWS_TABLE, 'title'):
            bs1.packaging_mes(news['title'], news['link'])
    bs1.send_message(config.WX_CRT_NEWS, config.WX_AGTID_NEWS)


def get_weibo():
    robot001.connectpage('https://s.weibo.com/top/summary?cate=realtimehot')
    weibo_item = robot001.get_items('#pl_top_realtimehot > table:nth-child(1) > tbody:nth-child(2) a')
    bs1.clear_arr()
    item_count = 0
    for item in weibo_item:
        item_count += 1
        if item_count == 10:
            break
        weibo = {
            'title': item.text(),
            'link': 'https://s.weibo.com' + item.attr('href'),
            'type': '微博'
        }
        if bs1.add_save_data(weibo, config.NEWS_TABLE, 'title'):
            bs1.packaging_mes(weibo['title'], weibo['link'])
    bs1.send_message(config.WX_CRT_NEWS, config.WX_AGTID_NEWS)


def main():
    get_weibo()
    parse_toutiao()
    parse_sport()


if __name__ == '__main__':
    main()
