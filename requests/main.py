import requests
import json
import uuid
import threading


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

a = _format(find(search))
print(a)
