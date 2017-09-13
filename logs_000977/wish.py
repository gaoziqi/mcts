import requests
import json

first='peter'
second='peter'
email='tdqs_abc@gmail.com'
password = '123456'

def register(first, second, email, password):
    url = 'https://www.wish.com'
    try:
        r = requests.get(url)
    except:
        return '网页打开失败'
    if r.status_code != 200:
        return '网页打开失败'
    url = 'https://www.wish.com/analytics/1519'
    headers = {
		'Accept': 'application/json, text/javascript, */*; q=0.01',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'zh-CN,zh;q=0.8',
		'Cookie':'_xsrf=%s;' % r.cookies['_xsrf'],
		'Connection':'keep-alive',
		'Content-Length':'99',
		'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
		'Host':'www.wish.com',
		'Origin':'https://www.wish.com',
		'Referer':'https://www.wish.com/',
		'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
		'X-Requested-With':'XMLHttpRequest',
		'X-Xsrftoken':r.cookies['_xsrf']
    }
    data = {'_app_type':'wish'}
    r = requests.post(url, data=json.dumps(data), headers=headers)
    if r.status_code != 200:
        return 'sweeper_uuid失败'
    url = 'https://www.wish.com/api/email-signup'
    headers['Cookie'] += ' bsid={0}; sweeper_uuid:{1}'.format(r.cookies['bsid'], json.loads(r.text)['sweeper_uuid'])
    data = 'first_name=%s&last_name=%s&email=%s&password=%s&_buckets=&_experiments=' % (first, second, email, password)
    r = requests.post(url, data=data, headers=headers)
    if r.status_code != 200:
        return '注册失败'
    else:
        return '注册成功'
