import tornado.ioloop
import tornado.web
from datetime import datetime
from _tushare import p, PRICE_MINUTES


class PredictHandler(tornado.web.RequestHandler):

    def get(self):
        now = datetime.now()
        _id = self.get_argument('code')
        _type = self.get_argument('type')
        start = self.get_argument('start', default=now.strftime('%Y-%m-%d 09:30:00'), strip=True)
        end = self.get_argument('end', default=now.strftime('%Y-%m-%d 15:05:00'), strip=True)
        if _id == '' or _type == '':
            raise tornado.web.HTTPError(404)
        print('%s -- PredictHandler: %s - code=%s, start=%s, end=%s' % (now.strftime('%Y-%m-%d %H:%M:%S'), self.request.remote_ip, _id, start, end))
        real = p._execute('''SELECT to_char(date,'YYYY-MM-DD HH24:MI:SS'), %s FROM %s WHERE code='%s' AND
            date>'%s' AND date<'%s' ORDER BY date''' % (_type, PRICE_MINUTES, _id, start, end))
        predict = p._execute('''SELECT to_char(date,'YYYY-MM-DD HH24:MI:SS'), %s FROM predict WHERE code='%s' AND
            date>'%s' AND date<'%s' ORDER BY date''' % (_type, _id, start, end))
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
], debug=True, **settings)


if __name__ == '__main__':
    app.listen(6791)
    tornado.ioloop.IOLoop.instance().start()
