import asyncio
from aiomysql import create_pool, SSCursor, DictCursor


loop = asyncio.get_event_loop()


class Service:
    async def _execute(self, query):
        async with create_pool(host='87.128.41.195', port=3306, user='root', password='toor', db='it-vision', loop=loop) as pool:
            async with pool.get() as connection:
                async with connection.cursor(DictCursor) as cursor:
                    await cursor.execute(query)
                    return await cursor.fetchall()