import hashlib
import time
import random
import json
from wish import register, login, collect

m5 = hashlib.md5()
with open('click.json','r') as r:
     click_url = json.load(r)

def baseN(num,b):
    return ((num == 0) and  "0" ) or ( baseN(num // b, b).lstrip("0") + "0123456789abcdefghijklmnopqrstuvwxyz"[num % b])

def get():
    m5.update(str(time.time()).encode('utf-8'))
    s = baseN(int(m5.hexdigest(),16), 36)
    a = random.randint(3,7)
    b = random.randint(5,12)
    first = s[0:a]
    second = s[a:a + b]
    email = '%s@gmail.com' % s[0:a + b]
    password = s[0:a + b]
    return first, second, email, password

def run(regist=False, w=None):
    if regist is False:
        first, second, email, password = get()
        try:
            r = register(first, second, email, password)
        except:
            return -1
        if r == 1:
            w.write('%s,' % password)
            w.flush()
        else:
            print(r)
            return -1
    try:
        with login(email, password) as s:
            for url in click_url:
                time.sleep(2)		# 相邻关注间隔时间
                print(collect(s, url, email))
    except:
        return -1
    return 1

k=0
with open('user.txt','w') as w:
    while(k < 10):
        if run(w=w)>0:
            k+=1
        else:
        	print("异常，失败")
        time.sleep(10)		# 相邻用户注册时间
print('谢谢使用，再也不见')
