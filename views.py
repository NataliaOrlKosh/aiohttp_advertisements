from aiohttp import web
from models import Advertisement


class AdvertisementView(web.View):

    async def get(self):
        advertisement_id = int(self.request.match_info['advertisement_id'])
        advertisement = await Advertisement.get_or_404(advertisement_id)
        return web.json_response(advertisement.to_dict())

    async def post(self):
        data = await self.request.json()
        advertisement = await Advertisement.create_instance(**data)
        return web.json_response(advertisement.to_dict())

    async def patch(self):
        instance_id = int(self.request.match_info['advertisement_id'])
        instance = await Advertisement.get_or_404(instance_id)
        data = await self.request.json()
        await instance.update(**data).apply()
        return web.json_response({'status': 'patched'})

    async def delete(self):
        instance_id = int(self.request.match_info['advertisement_id'])
        instance = await Advertisement.get_or_404(instance_id)
        await instance.delete()
        return web.json_response({'status': 'deleted'})


class AdvertisementsView(web.View):
    async def get(self):
        pool = self.request.app['pg_pool']
        async with pool.acquire() as conn:
            async with conn.cursor() as cursor:
                await cursor.execute('SELECT id, title, text FROM advertisements')
                advertisements = await cursor.fetchall()
                return web.json_response(advertisements)