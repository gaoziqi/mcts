import pandas as pd
import numpy as np
from datetime import datetime, timedelta
from base import Predict
from keras.models import model_from_json

period = 30
delay = 47


def predictDay(date, r, OCHL):
    k = 0
    for t in d:
        time = date + t
        print(time)
        p1 = []
        x = np.array(r[0].tail(delay + period - k).head(period))
        x = x.reshape([1, period, -1])
        for _id in codes:
            if stop[_id]:
                continue
            if _id not in OCHL:
                OCHL[_id] = np.array(r[1][['open_%s' % _id, 'close_%s' % _id,
                                           'high_%s' % _id, 'low_%s' % _id]])
            p0 = model.predict(x)
            OCHL[_id] = p0[0] / 100 + OCHL[_id]
            p1.append(np.append(OCHL[_id], _id))
        predict.inserts(time, p1)
        k += 1
    return OCHL


if __name__ == '__main__':
    version = 0
    predict = Predict()
    predict.delete()
    model = model_from_json(open('predict/model%d.json' % version).read())
    now = datetime.now()
    # now = now + timedelta(days=1)
    """codes = ('000977', '000021', '300076', '002312', '002635', '300130', '600271',
             '300367', '002528', '000066', '002177', '300282', '300390', '300042',
             '600734', '002376', '600601', '002180', '002351', '002308', '300045',
             '002362', '002152', '002577', '603019')"""
    codes = ['000977']
    stop = {}
    for i in codes:
        stop[i] = False
    """d = []
    d1 = datetime.strptime('09:35:00', '%H:%M:%S')
    d2 = datetime.strptime('11:35:00', '%H:%M:%S')
    d3 = datetime.strptime('13:05:00', '%H:%M:%S')
    d4 = datetime.strptime('15:05:00', '%H:%M:%S')
    while d1 < d2:
        d.append(d1.strftime('%H:%M:%S'))
        d1 = d1 + timedelta(minutes=5)
    while d3 < d4:
        d.append(d3.strftime('%H:%M:%S'))
        d3 = d3 + timedelta(minutes=5)"""
    d = ['09:35:00', '09:40:00', '09:45:00', '09:50:00', '09:55:00', '10:00:00',
         '10:05:00', '10:10:00', '10:15:00', '10:20:00', '10:25:00', '10:30:00',
         '10:35:00', '10:40:00', '10:45:00', '10:50:00', '10:55:00', '11:00:00',
         '11:05:00', '11:10:00', '11:15:00', '11:20:00', '11:25:00', '11:30:00',
         '13:05:00', '13:10:00', '13:15:00', '13:20:00', '13:25:00', '13:30:00',
         '13:35:00', '13:40:00', '13:45:00', '13:50:00', '13:55:00', '14:00:00',
         '14:05:00', '14:10:00', '14:15:00', '14:20:00', '14:25:00', '14:30:00',
         '14:35:00', '14:40:00', '14:45:00', '14:50:00', '14:55:00', '15:00:00']

    start = datetime.strptime('2017-08-16', '%Y-%m-%d')
    model.load_weights('predict/weight%d_%s.h5' % (version, codes[0]))
    OCHL = {}
    while start < now:
        if start.weekday() < 5:
            date = start.strftime('%Y-%m-%d') + ' '
            r = predict.get(start)
            OCHL = predictDay(date, r, OCHL)
        start = start + timedelta(days=1)
