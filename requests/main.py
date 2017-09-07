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
        r = requests.post(url, headers=headers, timeout=1)
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
        url1 = url.format(search, i, port[i], uuid.uuid1())
        t = threading.Thread(target=run, args=(url1,))
        t.setDaemon(True)
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    return _global().data


def _format(r):
    result = []
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

w = open('Result.csv', 'w')
w.write('箱号,箱型,码头名称,进场时间,出场时间,营运人,船名,车队,目的港\n')
for s in search:
    d = find(s)
    for a in d:
        r = _format(a)
        for b in r:
            w.write('%s\n' % b.__str__()
                    [1:-1].replace("'", ''))
    ii += 1
    print(ii)
w.close()
