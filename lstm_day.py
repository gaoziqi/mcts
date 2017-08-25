import os
import sys
import pandas as pd
import numpy as np
from keras.models import Sequential, model_from_json
from keras.layers import Dense, LSTM, Dropout
from keras.callbacks import TensorBoard

lstm_len = 64 if len(sys.argv) < 2 else int(sys.argv[1])
period = 20 if len(sys.argv) < 3 else int(sys.argv[2])
epochs = 300 if len(sys.argv) < 4 else int(sys.argv[3])
length = None


def build(period):
    model = Sequential()
    model.add(LSTM(lstm_len, return_sequences=True, input_shape=(period, length)))
    model.add(LSTM(lstm_len))
    model.add(Dropout(0.25))
    model.add(Dense(4))
    return model


def get(dt, step, _id):
    x = []
    y = []
    for i in range(len(dt) - step):
        x.append(np.array(dt[i:i + step]))
        y.append(np.array(dt.ix[i + step, ['open_%s' % _id, 'close_%s' % _id,
                                           'high_%s' % _id, 'low_%s' % _id]]))
    return np.array(x), np.array(y)


def lstm(r, _id, model, version, initial_epoch, epochs, period):
    x, y = get(r, period, _id)
    # model.load_weights('predict/weight%d_%s.h5' % (version, _id))
    model.compile(loss='mse', optimizer='adam')
    os.system('rm -rf logs_%d' % _id)
    cbks = [TensorBoard(log_dir='logs_%s' % _id, write_images=1, histogram_freq=1)]
    print('begin fit')
    model.fit(x, y, batch_size=16, initial_epoch=initial_epoch, epochs=initial_epoch + epochs, verbose=1, callbacks=cbks, validation_split=0.1)
    print('save weight')
    model.save_weights('predict/weight%d_%s.h5' % (version, _id))


_build = True
if __name__ == '__main__':
    version = 0
    initial_epoch = 0
    r = pd.read_csv('train_x.csv')
    r = r.fillna(-1)
    length = r.shape[1]
    model = build(period)
    #model = model_from_json(open('predict/model%d.json' % version).read())
    codes = ('000977', '000021', '300076', '002312', '002635', '300130', '600271',
             '300367', '002528', '000066', '002177', '300282', '300390', '300042',
             '600100', '600074', '600734', '002376', '600601', '002180', '002351',
             '002308', '300045', '002362', '002152', '002577', '603019')
    for _id in codes:
        lstm(r, _id, model, version, initial_epoch, epochs, period)
    print('success')
