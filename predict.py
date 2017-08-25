import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from base import Predict
#from keras.models import model_from_json

preriod = 6


def getDay(date, _id, conn, power=None):
    now = datetime.now().date()
    r = []
    if date < now:
        r = pd.read_sql('''SELECT a.f_value,d1.f_id as infod,d2.f_id as infon,
        b.f_tempd,b.f_tempn,c.f_vac
        FROM t_powerday as a,t_weatherls as b,t_workday as c,td_weather_info as d1, td_weather_info as d2
        WHERE a.f_date + interval '1 D' = b.f_date AND b.f_date=c.f_date AND b.f_statusd=d1.f_info AND b.f_statusn=d2.f_info
        AND f_devid='%s' AND b.f_date='%s'
        ''' % (_id, date), conn)
    elif date == now:
        r = pd.read_sql('''SELECT a.f_value,d1.f_id as infod,d2.f_id as infon,
        b.f_tempd,b.f_tempn,c.f_vac
        FROM t_powerday as a,t_forecast as b,t_workday as c,td_weather_info as d1, td_weather_info as d2
        WHERE a.f_date + interval '1 D' = b.f_date AND b.f_date=c.f_date AND b.f_statusd=d1.f_info AND b.f_statusn=d2.f_info
        AND f_devid='%s' AND b.f_date='%s'
        ''' % (_id, date), conn)
    else:
        r = pd.read_sql('''SELECT %f,d1.f_id as infod,d2.f_id as infon,
        b.f_tempd,b.f_tempn,c.f_vac
        FROM t_forecast as b,t_workday as c,td_weather_info as d1, td_weather_info as d2
        WHERE b.f_date=c.f_date AND b.f_statusd=d1.f_info AND b.f_statusn=d2.f_info
        AND b.f_date='%s'
        ''' % (power, date), conn)
    return np.array(r)


def predictDay(model, date, _id, conn, d=None, power=None):
    if d is None:
        d = []
        date1 = date - timedelta(days=preriod)
        while date1 < date:
            date1 += timedelta(days=1)
            d.append(getDay(date1, _id, conn))
        d = np.reshape(np.array(d), [1, preriod, 6])
    else:
        e = []
        e.append(getDay(date, _id, conn, power))
        e = np.append(d[0][1:], e)
        d = np.reshape(np.array(e), [1, preriod, 6])
    p = model.predict(d)
    return p[0][0], d


def predictWeek(model, date, _id, predict):
    start = date
    end = date + timedelta(days=7)
    p = None
    d = None
    while start < end:
        p, d = predictDay(model, start, _id, predict.conn, d=d, power=p)
        predict.insert(_id, p, start)
        start = start + timedelta(days=1)


if __name__ == '__main__':
    version = 0
    p = Predict()
    # p.delete()
    p.auto_update()
    """model = model_from_json(open('predict/model%d.json' % version).read())
    date = datetime.now().date()
    id_list = [27, 269, 270, 271, 272, 273]
    for _id in id_list:
        model.load_weights('predict/weight%d_%d.h5' % (version, _id))
        predictWeek(model, date, _id, p)"""
