import aiopg as aiopg
import pydantic
from aiohttp import web
from config import PG_DSN
from views import AdvertisementView, AdvertisementsView
from models import db


@web.middleware
async def validation_error_handler(request, handler):
    try:
        response = await handler(request)
    except pydantic.error_wrappers.ValidationError as er:
        response = web.json_response({'error': str(er)}, status=400)
    return response

app = web.Application(middlewares=[validation_error_handler])


async def set_connection():
    return await db.set_bind(PG_DSN)


async def disconnect():
    return await db.pop_bind().close()


async def orm_engine(app):
    app['db'] = db
    await set_connection()
    await db.gino.create_all()
    yield
    await disconnect()


async def pg_pool(app):
    async with aiopg.create_pool(PG_DSN) as pool:
        app['pg_pool'] = pool
        yield
        pool.close()


app.cleanup_ctx.append(orm_engine)
app.cleanup_ctx.append(pg_pool)

app.add_routes([web.get('/advertisements', AdvertisementsView),
                web.get(r'/advertisement/{advertisement_id:\d+}', AdvertisementView),
                web.post('/advertisement', AdvertisementView),
                web.patch(r'/advertisement/{advertisement_id:\d+}', AdvertisementView),
                web.delete(r'/advertisement/{advertisement_id:\d+}', AdvertisementView),
                ])