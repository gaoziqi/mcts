import tushare as ts
from sqlalchemy import create_engine
from base import Postgre

engine = create_engine('postgresql+psycopg2://postgres:tdq$abc123@127.0.0.1/tushare')
STOCK_BASICS = 'stock_basics'
PRICE_DAY = 'price_day'


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
    # sql_save(ts.get_k_data(code), 'H_%s' % code, engine)


def init(p):
    # get_stock_basics()
    codes = p._execute("SELECT CODE FROM %s WHERE INDUSTRY='电脑设备' AND \"timeToMarket\"<20150101 " % STOCK_BASICS)
    for i in codes:
        get_k_data_day(i[0])


if __name__ == '__main__':
    p = Postgre()
    init(p)

    print('success')
