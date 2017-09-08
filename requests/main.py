import requests
import json
import uuid
import threading
import time


class Global(object):
    """Global var"""
    __global = None

    def __init__(self):
        self.data = []
        self.mutex = False  # 线程间安全锁
        self.process = 15  # 开启线程数量
        self.period = 5  # 连续访问间隔时间

    def stop(self):
        if len(self.data) > 0:
            return True
        else:
            return False

    @staticmethod
    def get_instance():
        if Global.__global is None:
            Global.__global = Global()
        return Global.__global


def _global():
    return Global.get_instance()


with open('port.json', 'r') as r:
    port = json.load(r)

with open('number.json', 'r') as r:
    search = json.load(r)


headers = {
    'Accept': '*/*',
    'Accept-Encoding': 'gzip, deflate, sdch, dr',
    'Accept-Language': 'zh-CN,zh;q=0.8',
    'Cache-Control': 'no-cache',
    'Connection': 'leep-alive',
    'Host': 'www.chinaports.com',
    'Origin': 'http://www.chinaports.com',
    'Referer': 'http://www.chinaports.com/containerTracker',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
        like Gecko) Chrome/54.0.2840.71 Safari/537.36'
}

url = "http://www.chinaports.com/containerTracker/allresult2/{0}/0/{1}/{2}/{3}"


def run(url):
    try:
        # timeout 每个线程的最大等待时间，建议不要小于5秒，有些港口数据需要40秒才能返回，如果要爬取全部数据建议大于60
        r = requests.post(url, headers=headers, timeout=5)
        if r.status_code == 200:
            try:
                if r.text != {}:
                    result = json.loads(r.text)['data']
                    if result and result['resultList'] and len(result['resultList']) > 0:
                        _global().data.append(result)
            except:
                print(r.text)
    except:
        pass


def find(search):
    threads = []
    _global().data = []
    for i in port:
        # 由于有50个港口，一共开启50个线程同时查询
        url1 = url.format(search, i, port[i], uuid.uuid1())
        t = threading.Thread(target=run, args=(url1,))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for t in threads:
        # 等待所有线程执行结束
        t.join()
    return _global().data


def _format(r):
    result = []
    # 结果格式化（输出数据的格式）
    for i in r['resultList']:
        result.append((
            i['xianghao'],
            i['xiangxing'],
            r['port_name'],
            i['jinchangtime'],
            i['chuchangtime'],
            i['yingyunren'],
            i['shipname'],
            i['chedui'],
            i['mudigang']
        ))
    return result


ii = 0
ff = 0
w = open('result.csv', 'w')   # 结果保存文件名
w1 = open('error.json', 'w')  # 爬取失败或无数据的箱号
w.write('箱号,箱型,码头名称,进场时间,出场时间,营运人,船名,车队,目的港\n')
w1.write('[')
dot = ''
search = search[7000:7100]
print(len(search))  # 爬取集装箱总数
for s in search:
    finish = False
    d = find(s)
    for a in d:
        r = _format(a)
        for b in r:
            finish = True
            w.write('%s\n' % b.__str__()
                    [1:-1].replace("'", ''))
    ii += 1
    print(ii)  # 当前爬取了几个
    if not finish:
        ff += 1
        w1.write('%s"%s"' % (dot, s))
        dot = ','
        w1.flush()
    w.flush()
    time.sleep(1)  # 相邻两个港口查询间隔，如果timeout很小，建议增加间隔，预防ip被封（ip被封一般也就一小时左右）
w.close()
w1.write(']')
w1.close()
print(ff)   # 爬取失败或没数据总数
