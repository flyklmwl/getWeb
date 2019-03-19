from datetime import datetime
from Config import config
from Tools import robot
from Tools import BackServer
from pyquery import PyQuery as pq
import random

robot001 = robot.Robot("www.baidu.com")
bs = BackServer.BackServer(
    config.WORK_URL,
    config.WORK_DB,
    config.WORK_TABLE,
    config.WX_CRT_WORK,
    config.WX_AGTID_WORK
)
agents = random.sample(config.agent, 1)
headers = {
    'Accept': 'application/json, text/javascript, */*; q=0.01',
    'Referer': 'https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch='
               'true&labelWords=&suginput=',
    'User-Agent': str(agents)
}


def parse():
    bs.clear_arr()
    print("开始解析网页")
    url = 'https://fe-api.zhaopin.com/c/i/sou'
    para = {
        'pageSize': '90',
        'cityId': '749',
        'industry': '10100',
        'workExperience': '-1',
        'education': '-1',
        'companyType': '-1',
        'employmentType': '-1',
        'jobWelfareTag': '-1',
        'kt': '3',
        '_v': '0.06974364'
    }
    result = robot001.connectpage(url, params=para)
    appid = result.json()['data']['results']
    for i in range(0, 10):
        work = {
            'jobName': appid[i]['jobName'],
            'updateDate': datetime.strptime(appid[i]['updateDate'], '%Y-%m-%d %H:%M:%S'),
            'positionURL': appid[i]['positionURL'],
            'salary': appid[i]['salary'],
            'id': appid[i]['number'],
            'companyName': appid[i]['company']['name'],
            'link': 'https://jobs.zhaopin.com/' + appid[i]['number'] + '.htm'
        }
        if bs.save_data(work, 'id'):
            bs.packaging_mes(work['jobName'], str(work['updateDate']), work['salary'], work['companyName'], work['link'])
    bs.send_message()


def parse_lagou(*args):             # 第一个参数是城市,第二个是关键字
    bs.clear_arr()
    print("开始解析网页")
    robot001.connectpage("https://www.lagou.com/jobs/list_运维", headers=headers, timeout=5)

    # cookie = result.cookies   # 在open_session中的不需要重新加载cookies了
    # print(cookie)
    url = 'https://www.lagou.com/jobs/positionAjax.json'
    if len(args) == 1:
        para = {
            'city': args[0],
            'needAddtionalResult': 'false'
        }
    else:
        para = {
            'city': args[0],
            'needAddtionalResult': 'false',
            'kd': args[1]
        }

    result = robot001.connectpage(url, 'utf-8', params=para, headers=headers, timeout=5)
    appid = result.json()['content']['positionResult']['result']
    for i in range(0, 10):
        work = {
            'jobName': appid[i]['positionName'],
            'updateDate': datetime.strptime(appid[i]['createTime'], '%Y-%m-%d %H:%M:%S'),
            'id': appid[i]['positionId'],
            'salary': appid[i]['salary'],
            'companyName': appid[i]['companyFullName'],
            'link': 'https://www.lagou.com/jobs/' + str(appid[i]['positionId']) + '.html'
        }
        if bs.save_data(work, 'id'):
            bs.packaging_mes(work['jobName'], str(work['updateDate']), work['salary'], work['companyName'], work['link'])
    bs.send_message()


def parse_zhipin():
    para = {
        'query': '',
        'city': '101250100',
    }
    robot001.connectpage('https://www.zhipin.com/job_detail/', params=para, headers=headers)
    items = robot001.get_items('.job-list > ul:nth-child(3) li')

    for item in items:
        part_doc = pq(item)
        name = part_doc('.job-title').text()
        print(name)

        link = part_doc('a').attr('href')
        print(link)

        salary = part_doc('.red').text()
        print(salary)

        company = part_doc('.company-text a').text()
        print(company)

        work = {
            'jobName': name,
            'updateDate': datetime.now(),
            'id': link,
            'salary': salary,
            'companyName': company,
            'link': 'https://www.zhipin.com' + link
        }
        if bs.save_data(work, 'id'):
            bs.packaging_mes(work['jobName'], str(work['updateDate']), work['salary'], work['companyName'],
                             work['link'])
    bs.send_message()


def main():
    parse_zhipin()
    parse()
    parse_lagou('长沙')
    parse_lagou('深圳', '设计')


if __name__ == '__main__':
    main()
