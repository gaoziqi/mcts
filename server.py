import tornado.ioloop
import tornado.web
import os
from datetime import datetime, timedelta



class PredictHandler(tornado.web.RequestHandler):

    def get(self):
        now = datetime.now()
        _id = self.get_argument('id')
        start = self.get_argument('start', default="2017-08-11", strip=True)
        end = self.get_argument('end', default=now.strftime('%Y-%m-%d'), strip=True)
        if _id == '':
            raise tornado.web.HTTPError(404)
        print('%s -- PredictHandler: %s - id=%s, start=%s, end=%s' % (now.strftime('%Y-%m-%d %H:%M:%S'), self.request.remote_ip, _id, start, end))
        p = Predict()
        real = p.get(_id, start, end)
        predict = []
        for i in range(7):
            predict.append(p.get(_id, start, end, True, i))
        kwargs = {
            'JS': 'js',
            'predict': predict,
            'real': real,
            'id': _id
        }
        self.render('server/html/predict.html', **kwargs)


settings = {
    'static_path': 'server',
    'static_url_prefix': '/server/',
}


app = tornado.web.Application([
    (r'/predict', PredictHandler),
], debug=False, **settings)


if __name__ == '__main__':
    app.listen(6791)
    tornado.ioloop.IOLoop.instance().start()
