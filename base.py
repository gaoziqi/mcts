import os
import psycopg2
import requests
import json
import pandas as pd
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta

codes = ('000977', '000021', '300076', '002312', '002635', '300130', '600271',
         '300367', '002528', '000066', '002177', '300282', '300390', '300042',
         '600734', '002376', '600601', '002180', '002351', '002308', '300045',
         '002362', '002152', '002577', '603019')


class Postgre(object):

    def __init__(self, conn=None):
        if conn:
            self.conn = conn
        else:
            self.conn = psycopg2.connect(database='tushare', user='postgres', password='tdq$abc123', host='172.16.10.51', port='5432')
        self.cu = self.conn.cursor()
        self.table = ''

    def _execute(self, sql):
        self.cu.execute(sql)
        return self.cu.fetchall()

    def _commit(self, sql):
        self.cu.execute(sql)
        self.conn.commit()

    def delete(self):
        self._commit("DELETE FROM %s;" % self.table)

    def drop(self):
        self._commit("DROP TABLE %s" % self.table)

    def close(self):
        self.conn.close()


class WeatherLS(Postgre):

    def __init__(self, conn=None):
        super(WeatherLS, self).__init__(conn)
        self.table = 't_weatherls'

    def create(self):
        sql = '''CREATE TABLE t_weatherls (
            f_date date,
            f_statusd character varying(4),
            f_statusn character varying(4),
            f_tempd integer,
            f_tempn integer,
            f_windpd character varying(8),
            f_windpn character varying(8),
            f_windfd character varying(8),
            f_windfn character varying(8),
            CONSTRAINT t_weatherls_pkey PRIMARY KEY (f_date));'''
        self._commit(sql)

    def insert(self, w, check=True):
        if check:
            r = self._execute("SELECT f_tempd FROM t_weatherls WHERE f_date='%s'" % w.date.strftime('%Y-%m-%d'))
            if r:
                return
        self._commit("INSERT INTO t_weatherls VALUES ('%s','%s','%s',%d,%d,'%s','%s','%s','%s')"
                     % (w.date.strftime('%Y-%m-%d'), w.status[0], w.status[1], w.temp[0], w.temp[1],
                        w.windp[0], w.windp[1], w.windf[0], w.windf[1]))

    def getOneDay(self, datetime, check=True):
        url = "http://www.tianqihoubao.com/lishi/xiqing/%s.html" % datetime.strftime('%Y%m%d')
        request = requests.get(url)
        r = request.text
        r = r[r.find('<table'):r.find('</table>')]
        w = Weather()
        w.getTable(r, datetime)
        self.insert(w, check)
        return datetime + timedelta(days=1)


class WeatherSS(Postgre):

    def __init__(self, conn=None):
        super(WeatherSS, self).__init__(conn)
        self.table = 't_weatherss'

    def create(self):
        sql = '''CREATE TABLE t_weatherss (
            f_time timestamp without time zone,  --插入时间
            f_publish_time timestamp without time zone,  --更新时间
            f_temperature double precision,  --气温
            f_airpressure double precision,  --气压
            f_humidity double precision,  --相对湿度（单位：％）
            f_rain double precision,  --降雨 (单位：％)
            f_rcomfort integer,  --？？？未知
            f_icomfort integer,  --舒适度
            f_info character varying(8),  --天气情况
            f_feelst double precision,  --体感温度
            f_direct character varying(8),  --风向
            f_power character varying(8),  --风力
            f_speed double precision,  --风速 (单位：m/s)
            CONSTRAINT t_weatherss_pkey PRIMARY KEY (f_time));'''
        self._commit(sql)

    def insert(self, r):
        w = r['weather']
        d = r['wind']
        self._commit("INSERT INTO t_weatherss VALUES (now(),'%s',%f,%f,%f,%f,%d,%d,'%s',%f,'%s','%s',%f)"
                     % (r['publish_time'], w['temperature'], w['airpressure'], w['humidity'], w['rain'],
                        w['rcomfort'], w['icomfort'], w['info'], w['feelst'], d['direct'], d['power'], d['speed']))

    def get(self):
        url = "http://www.nmc.cn/f/rest/real/54527"
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, sdch',
            'Accept-Language': 'zh-CN,zh;q=0.8',
            'Cache-Control': 'max-age=0',
            'Host': 'www.nmc.cn',
            'Referer': 'http://www.nmc.cn/publish/forecast/ATJ/xiqing.html',
            'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWekit/537.36 (KHTML,\
            like Gecko) Chrome/54.0.2840.71 Safari/537.36'
        }
        request = requests.get(url, headers=headers)
        r = json.loads(request.text)
        self.insert(r)


class Forecast(Postgre):

    def __init__(self, conn=None):
        super(Forecast, self).__init__(conn)
        self.table = 't_forecast'

    def create(self):
        sql = '''CREATE TABLE t_forecast (
            f_id integer,
            f_date date,
            f_statusd character varying(4),
            f_statusn character varying(4),
            f_tempd integer,
            f_tempn integer,
            f_windpd character varying(8),
            f_windpn character varying(8),
            f_windfd character varying(8),
            f_windfn character varying(8),
            CONSTRAINT t_forecast_pkey PRIMARY KEY (f_id));'''
        self._commit(sql)

    def update(self, d):
        i = 0
        for w in d:
            self._commit('''UPDATE t_forecast SET f_date='%s',f_statusd='%s',f_statusn='%s',
                f_tempd=%d,f_tempn=%d,f_windpd='%s',f_windpn='%s',f_windfd='%s',f_windfn='%s' WHERE f_id=%d
                ''' % (w.date.strftime('%Y-%m-%d'), w.status[0], w.status[1], w.temp[0], w.temp[1],
                       w.windp[0], w.windp[1], w.windf[0], w.windf[1], i))
            i += 1

    def get(self):
        url = "http://www.nmc.cn/publish/forecast/ATJ/xiqing.html"
        request = requests.get(url)
        r = request.text.encode(request.encoding).decode('utf-8')
        r = r[r.find('<div id="forecast" class="forecast">'):r.find('<div id="hour3">')]
        p = r.find('</tbody>')
        date = datetime.now().date()
        d = []
        while p > 0:
            w = Weather()
            date = w.getForecast(r[r.find('<tbody>') + 7:p], date)
            r = r[p + 8:-1]
            p = r.find('</tbody>')
            d.append(w)
        self.update(d)


class AQI(Postgre):

    def __init__(self, conn=None):
        super(AQI, self).__init__(conn)
        self.table = 't_aqi'

    def create(self):
        sql = '''CREATE TABLE t_aqi (
            f_date date,
            f_level character varying(4),
            f_aqi integer,
            f_range integer,
            f_pm2_5 integer,
            f_pm10 integer,
            f_so2 integer,
            f_no2 integer,
            f_co double precision,
            f_o3 integer,
            CONSTRAINT t_aqi_pkey PRIMARY KEY (f_date));'''
        self._commit(sql)

    def insert(self, a, check=True):
        if check:
            r = self._execute("SELECT f_aqi FROM t_aqi WHERE f_date='%s'" % a.date)
            if r:
                return
        self._commit("INSERT INTO t_aqi VALUES ('%s','%s',%d,%d,%d,%d,%d,%d,%f,%d)"
                     % (a.date, a.level, a.aqi, a.rank, a.pm2_5, a.pm10,
                        a.so2, a.no2, a.co, a.o3))

    def getMonth(self, date, check=True):
        url = 'http://www.tianqihoubao.com/aqi/tianjin-%s.html' % date.strftime('%Y%m')
        r = requests.get(url).text
        r = r[r.find('<table'):r.find('</table>')]
        r = r[r.find('</tr>') + 5:-1]
        p = r.find('</tr>')
        while (p > 0):
            a = self._AQI()
            a.getTable(r[0:p])
            r = r[r.find('</tr>') + 5:-1]
            p = r.find('</tr>')
            self.insert(a)
        return date + relativedelta(months=1)

    class _AQI(object):

        def __init__(self):
            self.date = ''
            self.level = ''
            self.aqi = -1
            self.rank = -1
            self.pm2_5 = -1
            self.pm10 = -1
            self.so2 = -1
            self.no2 = -1
            self.co = -1
            self.o3 = -1

        def __str__(self):
            return 'date: %s\nlevle: %s\naqi: %d\nrank: %d\npm2.5: %d\npm10: %d\nso2: %d\nno2: %d\nco: %f\no3: %d\
            ' % (self.date, self.level, self.aqi, self.rank, self.pm2_5, self.pm10,
                 self.so2, self.no2, self.co, self.o3)

        def getTable(self, t):
            t = t[t.find('<td') + 3:-1]
            self.date = t[t.find('>') + 1:t.find('</td>')].strip()
            t = t[t.find('<td') + 3:-1]
            self.level = t[t.find('>') + 1:t.find('</td>')].strip()
            t = t[t.find('<td') + 4:-1]
            self.aqi = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.rank = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.pm2_5 = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.pm10 = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.so2 = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.no2 = int(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.co = float(t[0:t.find('</td>')])
            t = t[t.find('<td') + 4:-1]
            self.o3 = int(t[0:t.find('</td>')])


class Predict(Postgre):

    def __init__(self, conn=None):
        super(Predict, self).__init__(conn)
        self.table = 'predict'

    def create(self):
        sql = '''CREATE TABLE predict (
            id serial,
            date timestamp without time zone,
            open double precision,
            close double precision,
            high double precision,
            low double precision,
            volume double precision,
            code text,
            CONSTRAINT predict_pkey PRIMARY KEY (id));'''
        self._commit(sql)

    def delete(self):
        self._commit("DELETE FROM predict;SELECT SETVAL('predict_id_seq',1,false)")

    def inserts(self, time, data):
        sql = ''
        sql1 = "INSERT INTO predict (date,open,close,high,low,code) VALUES ('{0}',%s,%s,%s,%s,'%s');".format(time)
        for i in data:
            sql += sql1 % (i[0], i[1], i[2], i[3], i[4])
        self._commit(sql)

    def get(self, time=datetime.now()):
        now = time.strftime('%Y-%m-%d %H:%M:%S')
        sql0 = 'WITH '
        sql1 = "SELECT EXTRACT(HOUR FROM date) * 60 + EXTRACT(MINUTE FROM date) AS time,"
        sql2 = 'FROM M_{0} '.format(codes[-1])
        for i in codes:
            sql0 += '''M_{1} AS (SELECT date,open as open_{1},
                close as close_{1},high as high_{1},low as low_{1},volume / 10000 as volume_{1}
                FROM {0} WHERE CODE='{1}' AND date>'2017-08-10' AND date<'{2}'),'''.format('price_minutes', i, now)
            sql1 += 'open_{0},close_{0},high_{0},low_{0},volume_{0},'.format(i)
            sql2 += 'FULL JOIN M_{0} USING(date) '.format(i)
        sql = '%s %s %s ORDER BY date' % (sql0[:-1], sql1[:-1], sql2[:-32])
        df = pd.read_sql(sql, self.conn)
        df = df.fillna(method='pad')
        df = df.fillna(method='bfill')
        OCHL = df.tail(1)
        t = df['time']
        df = df.rolling(2).apply(lambda x: x[1] - x[0])
        df = df * 100
        df['time'] = t
        df = df.drop(0)
        return df, OCHL


class Weather(object):

    def __init__(self):
        self.date = None
        self.status = ['', '']  # 天气
        self.temp = [0, 0]  # 温度
        self.windp = ['', '']  # 风力
        self.windf = ['', '']  # 风向

    def __str__(self):
        return 'date: %s\nstatus: %s / %s\ntemp: %d / %d\nwindp: %s / %s\nwindf: %s / %s\
            ' % (self.date, self.status[0], self.status[1], self.temp[0], self.temp[1],
                 self.windp[0], self.windp[1], self.windf[0], self.windf[1])

    def getTable(self, table, datetime):
        self.date = datetime
        t = table[table.find("alt='") + 5: -1]
        self.status[0] = t[0:t.find("'")]
        t = t[t.find("alt='") + 5: -1]
        self.status[1] = t[0:t.find("'")]
        t = t[t.find('color:') + 6:-1]
        self.temp[0] = int(t[t.find('<b>') + 3:t.find('℃</b>')])
        t = t[t.find('color:') + 6:-1]
        self.temp[1] = int(t[t.find('<b>') + 3:t.find('℃</b>')])
        t = t[t.find('风力风向'):-1]
        t = t[t.find('<td>') + 4:-1]
        self.windf[0] = t[0:t.find(' ')]
        self.windp[0] = t[t.find(' ') + 1:t.find('</td>')]
        t = t[t.find('<td>') + 4:-1]
        self.windf[1] = t[0:t.find(' ')]
        self.windp[1] = t[t.find(' ') + 1:t.find('</td>')]

    def getForecast(self, t, datetime):
        self.date = datetime
        r = '<td class="wdesc">'
        t = t[t.find(r) + len(r):-1]
        self.status[0] = t[0:t.find('</td>')]
        t = t[t.find(r) + len(r):-1]
        self.status[1] = t[0:t.find('</td>')]
        r = '<td class="temp">'
        t = t[t.find(r) + len(r):-1]
        self.temp[0] = int(t[0:t.find('℃ </td>')])
        t = t[t.find(r) + len(r):-1]
        self.temp[1] = int(t[0:t.find('℃ </td>')])
        r = '<td class="direct">'
        t = t[t.find(r) + len(r):-1]
        self.windf[0] = t[0:t.find('</td>')]
        t = t[t.find(r) + len(r):-1]
        self.windf[1] = t[0:t.find('</td>')]
        r = '<td class="power">'
        t = t[t.find(r) + len(r):-1]
        self.windp[0] = t[0:t.find('</td>')]
        t = t[t.find(r) + len(r):-1]
        self.windp[1] = t[0:t.find('</td>')]
        return datetime + timedelta(days=1)
