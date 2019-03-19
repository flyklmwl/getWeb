from Config import config
from Tools import robot
from Tools import BackServer
from datetime import datetime


robot001 = robot.Robot("http://www.baidu.com")
bs1 = BackServer.BackServer(
    config.NEWS_URL,
    config.NEWS_DB,
    config.NEWS_TABLE,
    config.WX_CRT_NEWS,
    config.WX_AGTID_NEWS
)
headers = {
    'x-api-version': '3.0.89',
    'x-app-version': '5.26.2',
    'x-app-za': 'OS=Android&Release=8.0.0&Model=SM-G9500&VersionName=5.26.2&VersionCode=913&Product=com.zhihu.android&Width=1080&Height=2076&Installer=%E5%BA%94%E7%94%A8%E5%AE%9D&DeviceType=AndroidPhone&Brand=samsung',
    'x-app-flavor': 'myapp',
    'x-app-build': 'release',
    'x-network-type': 'WiFi',
    'Host': 'api.zhihu.com',
    'User-Agent': 'com.zhihu.android/Futureve/5.26.2 Mozilla/5.0 (Linux; Android 8.0.0; SM-G9500 Build/R16NW; wv) AppleWebKit/537.36 (KHTML, like Gecko) Version/4.0 Chrome/67.0.3396.87 Mobile Safari/537.36',
    'Connection': 'keep-alive'
}


def parse_toutiao():
    result = robot001.connectpage("https://www.toutiao.com/api/pc/realtime_news/", 'utf-8')
    news = result.json()['data']
    bs1.clear_arr()
    if news:
        for i in range(0, 10):
            new = {
                'title': news[i]['title'],
                'link': "https://www.toutiao.com" + news[i]['open_url'],
                'type': "今日头条",
                'date': datetime.now()
                # 'time': time.localtime()
            }
            # result = robot001.connectpage(new['link'], 'utf-8')
            # get_date = robot001.get_item('.bui-box')
            # print(get_date)
            if bs1.save_data(new, 'link'):
                bs1.packaging_mes(new['type'], new['title'], new['link'])
        bs1.send_message()
    else:
        print("没有抓取到数据!")


def parse_sport():
    robot001.connectpage("http://sports.sina.com.cn/nba/", 'utf-8')
    news_items1 = robot001.get_items(".layout_sports_350_650 > div:nth-child(1) h3 a")
    # print(news_items1)
    bs1.clear_arr()
    if news_items1:
        for item in news_items1:
            news = {
                'title': item.text(),
                'link': item.attr('href'),
                'type': '新浪体育',
                'date': datetime.now()
            }
            if bs1.save_data(news, 'link'):
                bs1.packaging_mes(news['title'], news['link'])
        bs1.send_message()
    else:
        print("没有抓取到数据!")


def get_weibo():
    robot001.connectpage('https://s.weibo.com/top/summary')
    weibo_item = robot001.get_items('#pl_top_realtimehot > table:nth-child(1) > tbody:nth-child(2) a')
    bs1.clear_arr()
    item_count = 0
    if weibo_item:
        for item in weibo_item:
            item_count += 1
            if item_count == 10:
                break
            weibo = {
                'title': item.text(),
                'link': 'https://s.weibo.com' + item.attr('href'),
                'type': '微博',
                'date': datetime.now()
            }
            if bs1.save_data(weibo, 'link'):
                bs1.packaging_mes(weibo['title'], weibo['link'])
        bs1.send_message()
    else:
        print("没有抓取到数据!")


def parse_zhihu():
    result = robot001.connectpage('https://api.zhihu.com/topstory/hot-list?limit=10', 'gbk2312', headers=config.headers)
    appid = result.json()['data']
    for i in range(0, 10):
        news = {
            'hot': appid[i]['detail_text'],
            'title': appid[i]['target']['title'],
            'link': 'https://www.zhihu.com/question/' + str(appid[i]['target']['id'])
        }
        if bs1.save_data(news, 'link'):
            bs1.packaging_mes(news['title'], news['link'])
    bs1.send_message()


def main():
    parse_zhihu()
    get_weibo()
    parse_toutiao()
    parse_sport()


if __name__ == '__main__':
    main()
