from Tools import loggingset
import pymongo
import urllib.request
import json


class BackServer:
    # 搜索、插入、更新数据库、发送微信信息
    leave_arr = []  # 存储需要发送的数据
    send_arr = []   # 存储需要发送的信息

    def __init__(self, conurl, condb, contable, crt, agtid):
        self.conurl = conurl
        self.condb = condb
        self.contable = contable
        self.crt = crt
        self.agtid = agtid
        self.client = pymongo.MongoClient(conurl)
        self.db = self.client[condb]

    def search_mongodb(self, search_table, search_title, search_value):
        return self.db[search_table].count_documents({search_title: search_value})

    def save_to_mongodb(self, save_table, result):
        if self.db[save_table].insert_one(result):
            loggingset.logger.debug("inserted into table")

    def del_to_mongodb(self, save_table, del_title, del_value):
        if self.db[save_table].delete_one({del_title: del_value}):
            loggingset.logger.debug("delete document")

    def send_message(self, *args):
        if len(args) == 1:
            msg = {"content": args[0]}
        else:
            msg = {"content": " ".join(self.send_arr)}
            if not self.send_arr:
                loggingset.logger.info("需要发送的信息不存在")
                return

        corpid = "wxeb4380288018eb1c"
        corpsecret = self.crt
        url = "https://qyapi.weixin.qq.com"
        token_url = "%s/cgi-bin/gettoken?corpid=%s&corpsecret=%s" % (
            url,
            corpid,
            corpsecret,
        )
        token = json.loads(urllib.request.urlopen(token_url).read().decode())[
            "access_token"
        ]
        values = {
            "touser": "@all",
            "msgtype": "text",
            "agentid": self.agtid,  # 偷懒没有使用变量了，注意修改为对应应用的agentid
            "text": msg,  # 这里注意是把list中的所有字符串都转换成一个发送出去
            "safe": 0,
        }
        msges = bytes(json.dumps(values), "utf-8")
        send_url = "%s/cgi-bin/message/send?access_token=%s" % (url, token)
        respone = urllib.request.urlopen(
            urllib.request.Request(url=send_url, data=msges)
        ).read()
        x = json.loads(respone.decode())["errcode"]
        if x == 0:
            loggingset.logger.info("已将抓取信息发送到微信")
            if len(args) == 0:
                self.clear_arr()
        else:
            loggingset.logger.error("发送到微信失败")
            if len(args) == 0:
                self.clear_arr()

    def save_update_data(self, datalist, s_key):
        save_count = 0
        for data in datalist:
            if self.search_mongodb(self.contable, s_key, data[s_key]) < 1:
                self.save_to_mongodb(self.contable, data)
                self.leave_arr.append(data)
                save_count += 1
            else:
                self.del_to_mongodb(self.contable, s_key, data[s_key])
                self.save_to_mongodb(self.contable, data)
                loggingset.logger.debug("已经保存了该主题")
        loggingset.logger.info("已存数据：" + str(save_count) + "条")

    def save_data(self, datalist, s_key):
        save_count = 0
        for data in datalist:
            if self.search_mongodb(self.contable, s_key, data[s_key]) < 1:
                self.save_to_mongodb(self.contable, data)
                self.leave_arr.append(data)
                save_count += 1
            else:
                loggingset.logger.debug("已经保存了该主题")
        loggingset.logger.info("已存数据：" + str(save_count) + "条")

    def packaging_mes(self, *args):
        # for i in range(len(args)):
        #     if i == len(args) - 1:
        #         self.send_arr.append(args[i] + "\n" + "\n")
        #         break
        #     self.send_arr.append(args[i] + "\n")
        if self.leave_arr:
            for data in self.leave_arr:
                for i in range(len(args)):
                    if i == len(args) - 1:
                        self.send_arr.append(str(data[args[i]]) + "\n" + "\n")
                        break
                    self.send_arr.append(str(data[args[i]]) + "\n")

    def clear_arr(self):
        self.leave_arr = []
        self.send_arr = []
