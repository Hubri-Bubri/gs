
from .database import Service
import json


class User(Service):
    async def select(self, name, passw, appid):

        users = await self._execute(f'''
            SELECT users.id, users.userName, companies.access, applications.name, applications.image,
            applications.description, applications.label, applications.link
            FROM users JOIN companies ON companies.user=users.id
            JOIN applications ON applications.id=companies.application
            WHERE users.userName='{name}' AND users.password='{passw}' AND companies.companyId='{appid}';
        ''')
        print (users)
        return json.dumps(users)
        