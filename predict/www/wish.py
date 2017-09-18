import requests
import json

timeout=60
proxies = { 
    "http": "http://171.37.164.126:9797"
}


def register(first, second, email, password):
    url = 'https://www.wish.com'
    try:
        r = requests.get(url, timeout=timeout, proxies=proxies)
    except:
        return '%s 网页打开失败' % email
    if r.status_code != 200:
        return '%s 网页打开失败' % email
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
    r = requests.post(url, data=json.dumps(data), headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s sweeper_uuid失败' % email
    url = 'https://www.wish.com/api/email-signup'
    headers['Cookie'] += ' bsid={0}; sweeper_uuid:{1}'.format(r.cookies['bsid'], json.loads(r.text)['sweeper_uuid'])
    data = 'first_name=%s&last_name=%s&email=%s&password=%s&_buckets=&_experiments=' % (first, second, email, password)
    r = requests.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s 注册失败' % email
    else:
        return 1

def login(email, password):
    url = 'https://www.wish.com'
    s = requests.session()
    try:
        r = s.get(url, timeout=timeout, proxies=proxies)
    except:
        return '%s 网页打开失败' % email
    if r.status_code != 200:
        return '%s 网页打开失败' % email
    url = 'https://www.wish.com/api/email-login'
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
    data = 'email=%s&password=%s&_buckets=&_experiments=' % (email, password)
    r = s.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s 登录失败' % email
    else:
        return s

def collect(s, url, email):
    """r = s.get(url)
    if r.status_code != 200:
        return '%s 打开%s失败' % (email, url)"""
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-CN,zh;q=0.8',
        'Connection':'keep-alive',
        'Content-Length':'99',
        'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
        'Host':'www.wish.com',
        'Origin':'https://www.wish.com',
        'Referer':'https://www.wish.com/',
        'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36',
        'X-Requested-With':'XMLHttpRequest',
        'X-Xsrftoken':s.cookies['_xsrf']
    }
    p =  url[url.rfind('/') + 1:]
    if p.find('=')>0:
        p = p[p.find('=') + 1:]
    data = 'contest_id=%s&recommended_by=&_buckets=&_experiments=' % p
    url = 'https://www.wish.com/api/contest/enter'
    r = s.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s 关注%s失败' % (email, p)
    else:
        return '%s 关注%s成功' % (email, p)
