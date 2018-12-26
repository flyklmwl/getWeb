from Config import config
from Tools import robot
from Tools import BackServer
import time


robot001 = robot.Robot("http://www.ali213.net/news/pingce/")
bs = BackServer.BackServer(config.GAMETEST_URL, config.GAMETEST_DB, config.GAMETEST_TABLE)


def youxia_parse():
    robot001.connectpage("http://www.ali213.net/news/pingce/", 'utf-8')
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) '
                                   '> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a').text(),
        'link': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l > div:nth-child(1) '
                                  '> div.t3_l_one_l > div.one_l_con > div.one_l_con_tit > a').attr("href"),
        'create': '游侠',
        'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'score': robot001.get_item('body > div.npc_a > div.npc_t3 > div.t3_l '
                                   '> div:nth-child(1) > div.t3_l_one_r > div > span').text()
    }
    if bs.add_save_data(pcdata, config.GAMETEST_TABLE, 'title'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message(config.WX_CRT_GT, config.WX_AGTID_GT)


def _3dm_parse():
    robot001.connectpage("https://www.3dmgame.com/original_40_1/")
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('body > div.content.clear > div.Content_L '
                                   '> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a').text(),
        'link': robot001.get_item('body > div.content.clear > div.Content_L '
                                  '> div.yc_warp_list > ul > li:nth-child(1) > div.bt > a').attr('href'),
        'create': '3dm',
        'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'score': robot001.get_item('body > div.content.clear > div.Content_L '
                                   '> div.yc_warp_list > ul > li:nth-child(1) > div.net > div > div.p > a').text()
    }
    if bs.add_save_data(pcdata, config.GAMETEST_TABLE, 'title'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message(config.WX_CRT_GT, config.WX_AGTID_GT)


def ymxk_parse():
    robot001.connectpage("https://www.gamersky.com/review/", 'utf-8')
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block '
                                   '> ul > li:nth-child(1) > div.con > div.tit > a').text(),
        'link': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul '
                                  '> li:nth-child(1) > div.con > div.tit > a').attr('href'),
        'create': '游民星空',
        'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'score': robot001.get_item('body > div.Mid > div.Mid2 > div.Mid2_L > div.Mid2L_con.block > ul '
                                   '> li:nth-child(1) > div.pc > div').text()
    }
    if bs.add_save_data(pcdata, config.GAMETEST_TABLE, 'title'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message(config.WX_CRT_GT, config.WX_AGTID_GT)


def _17173pc_parse():
    robot001.connectpage('http://newgame.17173.com/game-demolist.html')
    bs.clear_arr()
    pcdata = {
        'title': robot001.get_item('#content > div.page-swsearch-main.search-mod > div.main > div.result-mod '
                                   '> div > ul > li:nth-child(1) > div.text > h3 > a').text(),
        'link': robot001.get_item('#content > div.page-swsearch-main.search-mod > div.main > div.result-mod '
                                  '> div > ul > li:nth-child(1) > div.text > h3 > a').attr('href'),
        'create': '17173pc',
        'date': time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())),
        'score': '没有......'
    }
    if bs.add_save_data(pcdata, config.GAMETEST_TABLE, 'title'):
        bs.packaging_mes(pcdata['title'], pcdata['link'])
    bs.send_message(config.WX_CRT_GT, config.WX_AGTID_GT)


def main():
    youxia_parse()
    _3dm_parse()
    ymxk_parse()
    _17173pc_parse()


if __name__ == '__main__':
    main()
