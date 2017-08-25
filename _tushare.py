import tushare as ts
import pandas as pd
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
    print(codes)
    for i in codes:
        # get_k_data_day(i[0])
        get_k_data_minute(i[0])


def create_train_x():
    codes = ('000977', '000021', '300076', '002312', '002635', '300130', '600271',
             '300367', '002528', '000066', '002177', '300282', '300390', '300042',
             '600100', '600074', '600734', '002376', '600601', '002180', '002351',
             '002308', '300045', '002362', '002152', '002577', '603019')
    sql0 = 'WITH '
    sql1 = "SELECT to_char(date, 'HH24:MI:SS') AS date,"
    sql2 = 'FROM M_{0} '.format(codes[-1])
    for i in codes:
        sql0 += '''M_{1} AS (SELECT date,open as open_{1},
            close as close_{1},high as high_{1},low as low_{1},volume as volume_{1}
            FROM {0} WHERE CODE='{1}' AND date>'2017-08-11'),'''.format(PRICE_MINUTES, i)
        sql1 += 'open_{0},close_{0},high_{0},low_{0},volume_{0},'.format(i)
        sql2 += 'FULL JOIN M_{0} USING(date) '.format(i)
    sql = '%s %s %s' % (sql0[:-1], sql1[:-1], sql2[:-32])
    df = pd.read_sql(sql, p.conn)
    df.to_csv('train_x.csv', index=False)


if __name__ == '__main__':
    # init()
    create_train_x()
    print('success')
