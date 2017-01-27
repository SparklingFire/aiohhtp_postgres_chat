import asyncio
import jinja2
import aiohttp_jinja2
import aiopg.sa
from aiohttp import web
from aiohttp_session import session_middleware
from aiohttp_session.cookie_storage import EncryptedCookieStorage
from settings import *
import aiohttp_debugtoolbar
from routes import routes_aggregator


async def close_pg(app):
    app['db'].close()
    await app['db'].wait_closed()


async def main(loop):
    middlewares = [session_middleware(EncryptedCookieStorage(SECRET_KEY)),
                   ]
    app = web.Application(loop=loop, middlewares=middlewares)
    aiohttp_debugtoolbar.setup(app)

    aiohttp_jinja2.setup(app,
                         loader=jinja2.FileSystemLoader('/home/dno/PycharmProjects/social_app/templates'),
                         context_processors=[])

    for route in routes_aggregator():
        app.router.add_route(route[0], route[1], route[2], name=route[3])
    app.router.add_static('/static', 'static', name='static')

    engine = await aiopg.sa.create_engine(
        database='social_app',
        user='test_user',
        password='test_password',
        host='localhost',
        port='5432',
        minsize=0,
        maxsize=100,
        loop=app.loop
    )

    app['db'] = engine
    app.on_cleanup.append(close_pg)

    handler = app.make_handler()
    server = loop.create_server(handler, '127.0.0.1', '8080')

    return app, server, handler


loop = asyncio.get_event_loop()
app, server, handler = loop.run_until_complete(main(loop))
srv = loop.run_until_complete(server)
print('---------------')
print('start server {0}'.format(str(srv.sockets[0].getsockname())))
print('---------------')
try:
    loop.run_forever()
except KeyboardInterrupt:
    pass
finally:
    print('---------------')
    print('shutting down the server')
    print('---------------')
    srv.close()
    loop.run_until_complete(srv.wait_closed())
    loop.run_until_complete(app.shutdown())
    loop.run_until_complete(handler.shutdown(10.0))
    loop.run_until_complete(app.cleanup())
loop.stop()
print('the server is down')
