import os
import sys
import pandas as pd
import numpy as np
from base import CSV
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import TensorBoard


_id = 27 if len(sys.argv) < 2 else int(sys.argv[1])
epochs = 300 if len(sys.argv) < 3 else int(sys.argv[2])
period = 6 if len(sys.argv) < 4 else int(sys.argv[3])


def build(period):
    model = Sequential()
    model.add(LSTM(64, return_sequences=True, input_shape=(period, 6)))
    model.add(LSTM(64))
    model.add(Dropout(0.1))
    model.add(Dense(1))
    return model


def get(dt, step):
    x = []
    y = []
    for i in range(len(dt) - step):
        x.append(np.array(dt[i:i + step]))
        y.append(np.array(dt.ix[i + step, ['f_value']]))
    return np.array(x), np.array(y)


def shuffle(x, y):
    if x.shape[0] != y.shape[0]:
        print("ERROR MUST BE EQUEL")
    index = np.arange(x.shape[0])
    np.random.shuffle(index)
    x1 = []
    y1 = []
    for i in index:
        x1.append(x[i])
        y1.append(y[i])
    return np.array(x1), np.array(y1)


_build = True
if __name__ == '__main__':
    version = 0
    initial_epoch = 0
    c = CSV()
    r = pd.read_sql('''SELECT b.f_date,a.f_value,d1.f_id as infod,d2.f_id as infon,
        b.f_tempd,b.f_tempn,c.f_vac
        FROM t_powerday as a,t_weatherls as b,t_workday as c,td_weather_info as d1, td_weather_info as d2
        WHERE a.f_date + interval '1 D' = b.f_date AND b.f_date=c.f_date AND b.f_statusd=d1.f_info AND b.f_statusn=d2.f_info
        AND a.f_date>'2017-06-06' AND f_devid='%s' ORDER BY b.f_date
        ''' % _id, c.conn)
    r1 = r.drop(['f_date'], 1)
    x, y = get(r1, step=period)
    x1, y1 = shuffle(x, y)
    print('begin')
    if _build:
        model = build(period)
    else:
        model = model_from_json(open('predict/model%d.json' % version).read())
        print('load weight')
        model.load_weights('predict/weight%d_%d.h5' % (version, _id))
    # model.compile(loss='mse', optimizer='adam', metrics=['accuracy'])
    model.compile(loss='mse', optimizer='adam')
    os.system('rm -rf logs_%d' % _id)
    cbks = [TensorBoard(log_dir='logs_%d' % _id, write_images=1, histogram_freq=1)]
    print('begin fit')
    model.fit(x1, y1, batch_size=2, initial_epoch=initial_epoch, epochs=initial_epoch + epochs, verbose=1, callbacks=cbks, validation_split=0.1)
    with open('predict/model%d.json' % version, 'w') as w:
        w.write(model.to_json())
    print('save weight')
    model.save_weights('predict/weight%d_%d.h5' % (version, _id))
    print('success')
