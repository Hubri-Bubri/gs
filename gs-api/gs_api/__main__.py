from asyncio import get_event_loop
import sqlalchemy

from gs_api.dictionary import User


user = User()

async def fetch_users():
    return await user.select()


if __name__ == '__main__':
    users = get_event_loop().run_until_complete(fetch_users())

    print(users)
