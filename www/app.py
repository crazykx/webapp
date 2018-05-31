import logging
import asyncio, os, json, time
from aiohttp import web
import aiomysql
logging.basicConfig(level=logging.INFO)


def index(request):
    return web.Response(body=b'<h1>Awesome</h1>',content_type='text/html')


@asyncio.coroutine
def init(loop):
    app = web.Application(loop=loop)
    app.router.add_route('GET', '/', index)
    srv = yield from loop.create_server(app.make_handler(), '127.0.0.1', 9000)
    logging.info('derver started at http://127.0.0.1:9000...')
    return srv


# 创建连接池 每个HTTP请求都可以从连接池中直接获取数据库连接
# 不必频繁打开和关闭数据库连接，能复用就尽量复用
@asyncio.coroutine
def create_pool(loop, **kw):
    logging.info('create database connection pool...')
    global  __pool
    __pool = yield from aiomysql.create_pool(
        host=kw.get('host', 'localhost'),
        port=kw.get('port', 3306),
        user=kw['password'],
        db=kw['db'],
        charset=kw.get('charset', 'utf8'),
        autocommit=kw.get('autocommit', True),
        maxsize=kw.get('maxsize', 10),
        minsize=kw.get('minsize', 1),
        loop=loop
    )

# select
@asyncio.coroutine
def select(sql, args, size=None):
    logging.log(sql, args)






loop = asyncio.get_event_loop()
loop.run_until_complete(init(loop))
loop.run_forever()