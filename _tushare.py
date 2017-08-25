import tushare as ts
from sqlalchemy import create_engine
from datetime import datetime
from base import Postgre

engine = create_engine('postgresql+psycopg2://postgres:tdq$abc123@127.0.0.1/tushare')
p = Postgre()
STOCK_BASICS = 'stock_basics'
PRICE_DAY = 'price_day'
PRICE_MINUTES = 'price_minutes'


def sql_save(df, name, engine, drop=False):
    try:
        if drop:
            df.to_sql(name, engine, if_exists='replace')
        else:
            df.to_sql(name, engine)
    except:
        print('%s is exists' % name)


def get_stock_basics():
    sql_save(ts.get_stock_basics(), STOCK_BASICS, engine, drop=True)


def get_k_data_day(code):
    print(code)
    a = ts.get_k_data(code)
    r = p._execute("SELECT MAX(date) FROM %s WHERE code='%s'" % (PRICE_DAY, code))
    now = datetime.now().strftime('%Y-%m-%d')
    if r and r[0][0]:
        a = a[(a['date'] > r[0][0].strftime('%Y-%m-%d')) & (a['date'] < now)]
    else:
        a = a[a['date'] < now]
    sql = ''
    sql1 = '''INSERT INTO {0} (date,open,close,high,low,volume,code)
    VALUES ('%s','%s','%s','%s','%s','%s','%s');'''.format(PRICE_DAY)
    for i in a.iterrows():
        sql += sql1 % tuple(i[1])
    if sql != '':
        p._commit(sql)


def get_k_data_minute(code):
    print(code)
    a = ts.get_k_data(code, ktype='5')
    r = p._execute("SELECT MAX(date) FROM %s WHERE code='%s'" % (PRICE_MINUTES, code))
    now = datetime.now().strftime('%Y-%m-%d %H:%M')
    if r and r[0][0]:
        a = a[(a['date'] > r[0][0].strftime('%Y-%m-%d %H:%M')) & (a['date'] < now)]
    else:
        a = a[a['date'] < now]
    sql = ''
    sql1 = '''INSERT INTO {0} (date,open,close,high,low,volume,code)
    VALUES ('%s','%s','%s','%s','%s','%s','%s');'''.format(PRICE_MINUTES)
    for i in a.iterrows():
        sql += sql1 % tuple(i[1])
    # print(sql)
    if sql != '':
        p._commit(sql)


def init():
    # get_stock_basics()
    codes = p._execute("SELECT CODE FROM %s WHERE INDUSTRY='电脑设备' AND \"timeToMarket\"<20150101 " % STOCK_BASICS)
    for i in codes:
        # get_k_data_day(i[0])
        get_k_data_minute(i[0])


if __name__ == '__main__':
    init()

    print('success')
