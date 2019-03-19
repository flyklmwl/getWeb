from Config import config
from Tools import robot
from Tools import BackServer
from datetime import datetime
import re
import json


robot001 = robot.Robot("http://www.ali213.net/news/pingce/")
bs = BackServer.BackServer(
    config.GAMETEST_URL,
    config.GAMETEST_DB,
    config.GAMETEST_TABLE,
    config.WX_CRT_GT,
    config.WX_AGTID_GT
)


def youxia_parse():
    robot001.connectpage("http://www.ali213.net/news/pingce/", 'utf-8')
    bs.clear_arr()
    get_date = re.search('.*时间：(.*)', robot001.get_item('.one_l_con_tag').text())

    pcdata = {
        'title': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) '
                                   '> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a').text(),
        'link': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) '
                                  '> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a').attr("href"),
        'create': '游侠',
        # 'date': datetime.now(),
        'date': datetime.strptime(get_date.group(1), "%Y-%m-%d"),
        'score': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l '
                                   '> div:nth-child(1) > div.t3_l_one_r > div > span').text()
    }
    print(pcdata['date'])
    print(type(pcdata['date']))
    if bs.save_data(pcdata, 'link'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message()


def _3dm_parse():
    robot001.connectpage("https://www.3dmgame.com/original_40_1/")
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('body > div.content.clear > div.Content_L '
                                   '> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a').text(),
        'link': robot001.get_item('body > div.content.clear > div.Content_L '
                                  '> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a').attr('href'),
        'create': '3dm',
        # 'date': datetime.now(),
        'date': datetime.strptime(robot001.get_item('.time').text()[:10], "%Y-%m-%d"),
        'score': robot001.get_item('body > div.content.clear > div.Content_L '
                                   '> div.yc_warp_list > ul > li:nth-child(1) > div.net > div > div.p > a').text()
    }
    if bs.save_data(pcdata, 'link'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message()


def ymxk_parse():
    robot001.connectpage("https://www.gamersky.com/review/", 'utf-8')
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block '
                                   '> ul > li:nth-child(1) > div.con > div.tit > a').text(),
        'link': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul '
                                  '> li:nth-child(1) > div.con > div.tit > a').attr('href'),
        'create': '游民星空',
        # 'date': datetime.now(),
        'date': datetime.strptime(robot001.get_item('.time').text()[:10], "%Y-%m-%d"),
        'score': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul '
                                   '> li:nth-child(1) > div.pc > div').text()
    }
    if bs.save_data(pcdata, 'link'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message()


def _17173pc_parse():
    robot001.connectpage('http://newgame.17173.com/game-demolist.html')
    bs.clear_arr()
    get_date = re.search('.*发表时间：(.*)', robot001.get_item('.date').text()[:15])
    pcdata = {
        'title': robot001.get_item('#content > div.page-swsearch-main.search-mod > div.main > div.result-mod '
                                   '> div > ul > li:nth-child(1) > div.text > h3 > a').text(),
        'link': robot001.get_item('#content > div.page-swsearch-main.search-mod > div.main > div.result-mod '
                                  '> div > ul > li:nth-child(1) > div.text > h3 > a').attr('href'),
        'create': '17173pc',
        # 'date': datetime.now(),
        'date': datetime.strptime(get_date.group(1), "%Y-%m-%d"),
        'score': '没有......'
    }
    print(pcdata['date'])
    if bs.save_data(pcdata, 'link'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message()


def _163_parse():
    result = robot001.connectpage('http://play.163.com/special/api_assess_all/').text
    result = result[14:][:-3]
    appid = json.loads(result)
    f_appid = appid[0]
    pcdata = {
        'title': f_appid['gameName'],
        'link': f_appid['url'],
        'create': '163',
        'date': datetime.now(),
        'score': f_appid['score']
    }
    if bs.save_data(pcdata, 'link'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message()


def main():
    _163_parse()
    youxia_parse()
    _3dm_parse()
    ymxk_parse()
    _17173pc_parse()


if __name__ == '__main__':
    main()
