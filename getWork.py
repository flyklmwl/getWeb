from datetime import datetime
from Config import config
from Tools import robot
from Tools import BackServer
from pyquery import PyQuery as pq
import random
import pysnooper


robot001 = robot.Robot("www.baidu.com")
bs = BackServer.BackServer(
    config.WORK_URL,
    config.WORK_DB,
    config.WORK_TABLE,
    config.WX_CRT_WORK,
    config.WX_AGTID_WORK,
)
agents = random.sample(config.agent, 1)
headers = {
    "Accept": "application/json, text/javascript, */*; q=0.01",
    "Referer": "https://www.lagou.com/jobs/list_%E8%BF%90%E7%BB%B4?city=%E6%88%90%E9%83%BD&cl=false&fromSearch="
    "true&labelWords=&suginput=",
    "User-Agent": str(agents),
}


# 智联招聘
def parse_zhilian():
    result = robot001.connectpage(
        "https://www.zhaopin.com/", headers=config.headers_zhilian, timeout=5
    )
    print(result)
    result = robot001.connectpage(
        "https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=749&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&=0&_v=0.92863347&x-zp-page-request-id=1f050eb41301413ea29a79df16c30006-1568167779956-514543&x-zp-client-id=2e65d455-b89a-4d60-ae58-40ae07293742", headers=config.headers_zhilian, timeout=5
    )
    print(result)


@pysnooper.snoop()
def parse():
    bs.clear_arr()
    print("开始解析网页")
    # url = "https://fe-api.zhaopin.com/c/i/sou"
    robot001.connectpage(
        "https://www.zhaopin.com/", headers=config.headers, timeout=5
    )

    url = "https://fe-api.zhaopin.com/c/i/sou?pageSize=90&cityId=749&salary=0,0&workExperience=-1&education=-1&companyType=-1&employmentType=-1&jobWelfareTag=-1&kt=3&=0&_v=0.92863347&x-zp-page-request-id=1f050eb41301413ea29a79df16c30006-1568167779956-514543&x-zp-client-id=2e65d455-b89a-4d60-ae58-40ae07293742"

    # para = {
    #     "pageSize": "90",
    #     "cityId": "749",
    #     "industry": "10100",
    #     "workExperience": "-1",
    #     "education": "-1",
    #     "companyType": "-1",
    #     "employmentType": "-1",
    #     "jobWelfareTag": "-1",
    #     "kt": "3",
    #     "_v": "0.06974364",
    # }

    # result = robot001.connectpage(url, params=para, headers=config.headers) 传params就报错,不传headers获取不到内容
    result = robot001.connectpage(url, headers=config.headers, timeout=5)
    appid = result.json()["data"]["results"]
    for i in range(0, 10):
        work = {
            "jobName": appid[i]["jobName"],
            "updateDate": datetime.strptime(
                appid[i]["updateDate"], "%Y-%m-%d %H:%M:%S"
            ),
            "positionURL": appid[i]["positionURL"],
            "salary": appid[i]["salary"],
            "id": appid[i]["number"],
            "companyName": appid[i]["company"]["name"],
            "link": "https://jobs.zhaopin.com/" + appid[i]["number"] + ".htm",
            "type": "zhilian"
        }
        if bs.save_data(work, "id"):
            bs.packaging_mes(
                work["jobName"],
                str(work["updateDate"]),
                work["salary"],
                work["companyName"],
                work["link"],
            )
    # bs.send_message()


@pysnooper.snoop()
def parse_lagou(*args):  # 第一个参数是城市,第二个是关键字
    bs.clear_arr()
    print("开始解析网页")
    robot001.connectpage(
        "https://www.lagou.com/jobs/list_运维", headers=headers, timeout=5
    )

    # cookie = result.cookies   # 在open_session中的不需要重新加载cookies了
    # print(cookie)
    url = "https://www.lagou.com/jobs/positionAjax.json"
    if len(args) == 1:
        para = {"city": args[0], "needAddtionalResult": "false"}
    else:
        para = {"city": args[0], "needAddtionalResult": "false", "kd": args[1]}

    result = robot001.connectpage(url, "utf-8", params=para, headers=headers, timeout=5)
    print(result.text)
    appid = result.json()["content"]["positionResult"]["result"]
    for i in range(0, 10):
        work = {
            "jobName": appid[i]["positionName"],
            "updateDate": datetime.strptime(
                appid[i]["createTime"], "%Y-%m-%d %H:%M:%S"
            ),
            "id": appid[i]["positionId"],
            "salary": appid[i]["salary"],
            "companyName": appid[i]["companyFullName"],
            "link": "https://www.lagou.com/jobs/"
            + str(appid[i]["positionId"])
            + ".html",
            "type": "lagou"
        }
        if bs.save_data(work, "id"):
            bs.packaging_mes(
                work["jobName"],
                str(work["updateDate"]),
                work["salary"],
                work["companyName"],
                work["link"],
            )
    bs.send_message()


@pysnooper.snoop()
def parse_zhipin():
    para = {"query": "", "city": "101250100"}
    result = robot001.connectpage(
        "https://www.zhipin.com/job_detail/",  params=para, headers=config.headers
    )
    items = robot001.get_items(".job-list > ul:nth-child(3) li")
    print(result.text)

    for item in items:
        part_doc = pq(item)
        name = part_doc(".job-title").text()
        print(name)

        link = part_doc("a").attr("href")
        print(link)

        salary = part_doc(".red").text()
        print(salary)

        company = part_doc(".company-text a").text()
        print(company)

        work = {
            "jobName": name,
            "updateDate": datetime.now(),
            "id": link,
            "salary": salary,
            "companyName": company,
            "link": "https://www.zhipin.com" + link,
            "type": "zhipin"
        }
        if bs.save_data(work, "id"):
            bs.packaging_mes(
                work["jobName"],
                str(work["updateDate"]),
                work["salary"],
                work["companyName"],
                work["link"],
            )
    bs.send_message()


def main():
    # parse_zhipin()
    # parse()
    # parse_zhilian()
    parse_lagou("长沙")
    # parse_lagou('深圳', '设计')


if __name__ == "__main__":
    main()
