import requests
import json
import uuid
import threading
import time


class Global(object):
    """Global var"""
    __global = None

    def __init__(self):
        self.data = {}
        self.mutex = False  # 线程间安全锁
        self.process = 15  # 开启线程数量
        self.period = 5  # 连续访问间隔时间

    @staticmethod
    def get_instance():
        if Global.__global is None:
            Global.__global = Global()
        return Global.__global


def _global():
    return Global.get_instance()


with open('port.json', 'r') as r:
    port = json.load(r)

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

search = 'RDMU2002133'
url = "http://www.chinaports.com/containerTracker/allresult2/{0}/0/{1}/{2}/{3}"


def run():
    while _global().mutex:
        time.sleep(1)
    _global().mutex = True
    _global().process -= 1
    _global().mutex = False


def find(search):
    result = None
    for i in port:
        url1 = url.format(search, i, port[i], uuid.uuid1())
        try:
            r = requests.post(url1, headers=headers, timeout=5)
        except:
            continue
        if r.status_code == 200:
            try:
                result = json.loads(r.text)['data']
            except:
                print(r.text)
            if result and result['resultList'] and len(result['resultList']) > 0:
                break
    print(result)
    return result


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

"""
while _global().process > process_max:
            time.sleep(5)
        t = threading.Thread(target=run_yt, args=(user, times))
        t.start()
        _global().mutex = True
        _global().process += 1
        _global().mutex = False
        i += 1
"""
a = _format(find(search))
print(a)
