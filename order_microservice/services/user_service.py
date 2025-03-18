from typing import Protocol

import requests


class UserService(Protocol):
   async def fetch_user_info(self, user_id: str) -> dict:
        ...

class UserServiceImpl(UserService):
    
    async def fetch_user_info(self, user_id: str) -> dict:
        response =  requests.get(f"http://user-service/api/users/{user_id}")
        return response.json()


