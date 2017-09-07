import requests
import json
import uuid


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
url1 = url.format(search, 49, port['49'], uuid.uuid1())
r = requests.post(url1, headers=headers)
if r.status_code == 200:
    a = json.loads(r.text)
    print(a)
