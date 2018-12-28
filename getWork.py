from Config import config
from Tools import robot
from Tools import BackServer
import json

robot001 = robot.Robot("www.baidu.com")
bs = BackServer.BackServer(config.WORK_URL, config.WORK_DB, config.WORK_TABLE)


def parse():
    print("开始解析网页")
    result = robot001.connectpage("https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=749&industry=10100&"
                                  "workExperience=-1&education=-1&companyType=-1&employmentType=-1&job"
                                  "WelfareTag=-1&kt=3&_v=0.06974364")
    print(type(result.text))
    appid = json.loads(result.text)['data']['results']
    for i in range(0, 10):
        # print(appid[i])
        work = {
            'jobName': appid[i]['jobName'],
            'updateDate': appid[i]['updateDate'],
            'positionURL': appid[i]['positionURL'],
            'salary': appid[i]['salary'],
            'id': appid[i]['SOU_POSITION_ID'],
            'companyName': appid[i]['company']['name'],
            'link': 'https://jobs.zhaopin.com/' + appid[i]['SOU_POSITION_ID'] + '.htm'
        }
        if bs.add_save_data(work, config.WORK_TABLE, 'id'):
            bs.packaging_mes(work['jobName'], work['updateDate'], work['salary'], work['companyName'], work['link'])
    bs.send_message(config.WX_CRT_WORK, config.WX_AGTID_WORK)


def main():
    parse()


if __name__ == '__main__':
    main()
