import requests
import json

timeout=60
proxies = { 
    "http": "http://171.37.164.126:9797"
}
first='peter'
second=''
email='tdqs_abc@gmail.com'
password='abc123'

def _getToken(t):
    r = t[t.find('" name="FORM_TOKEN"') - 100 :t.find('" name="FORM_TOKEN"')]
    r = r[r.find('value="') + 7:]
    return r

def register(first, second, email, password):
    url = 'https://www.lazada.com.my/customer/account/create/'
    with requests.session() as s:
        try:
            r = s.get(url, timeout=timeout, proxies=proxies)
        except:
            return '%s 创建用户失败' % email
        if r.status_code != 200:
            return '%s 创建用户失败' % email
        headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.lazada.com.my',
            'Origin':'https://www.lazada.com.my',
            'Referer':'https://www.lazada.com.my/customer/account/create',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        token = _getToken(r.text)
        data = "FORM_TOKEN={0}&RegistrationForm[gender]=&RegistrationForm[gender]=male&RegistrationForm[email]={1}&RegistrationForm[first_name]={2}&RegistrationForm[day]=&RegistrationForm[month]=&RegistrationForm[year]=&RegistrationForm[fk_language]=2&RegistrationForm[password]={3}&RegistrationForm[password2]={3}&RegistrationForm[is_newsletter_subscribed]=0&RegistrationForm[is_newsletter_subscribed]=1"
        data = data.format(token, email, first, password)
        r = s.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
        if r.status_code != 200:
            return '%s 注册失败' % email
        else:
            return 1

def login(email, password):
    url = 'https://www.lazada.com.my/customer/account/login/'
    s = requests.session()
    try:
        r = s.get(url, timeout=timeout, proxies=proxies)
    except:
        return '%s 登陆失败' % email
    if r.status_code != 200:
        return '%s 登陆失败' % email
    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.lazada.com.my',
            'Origin':'https://www.lazada.com.my',
            'Referer':'https://www.lazada.com.my/customer/account/login/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    token = _getToken(r.text)
    data = 'FORM_TOKEN={0}&referer=&LoginForm[email]={1}&LoginForm[password]={2}'.format(token, email, password)
    r = s.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s 登录失败' % email
    url = 'https://www.lazada.com.my/customer/wishlist/index/'
    try:
        r = s.get(url, timeout=timeout, proxies=proxies)
    except:
        return '%s 打开wishlist失败' % email
    if r.status_code != 200:
        return '%s 打开wishlist失败' % email
    headers = {
            'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding':'gzip, deflate, br',
            'Accept-Language':'zh-CN,zh;q=0.8',
            'Cache-Control':'max-age=0',
            'Connection':'keep-alive',
            'Content-Type':'application/x-www-form-urlencoded',
            'Host':'www.lazada.com.my',
            'Origin':'https://www.lazada.com.my',
            'Referer':'https://www.lazada.com.my/customer/wishlist/index/',
            'Upgrade-Insecure-Requests':'1',
            'User-Agent':'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/54.0.2840.71 Safari/537.36'
    }
    token = _getToken(r.text)
    data = 'FORM_TOKEN={0}&WishlistForm[status]=shared&WishlistForm[name]={1}'.format(token, password)
    r = s.post(url, data=data, headers=headers, timeout=timeout, proxies=proxies)
    if r.status_code != 200:
        return '%s 添加wishlist失败' % email
    else:
        return s

def collect(s, url, email):
    r = s.get(url)
    if r.status_code != 200:
        return '%s 打开%s失败' % (email, url)
    

"configSku=OE702HLDNDTXANMY&simpleSku=OE702HLDNDTXANMY-4998530&id_wishlist=1873802&isAjax=true&FORM_TOKEN=42790324efc9d185870f89f93d525775d591b9c8&_=1505447296838"