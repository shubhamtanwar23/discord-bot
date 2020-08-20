from typing import List

import aioredis
from aioredis.commands import Redis

from settings import settings
from storage import StorageManager


class RedisManager(StorageManager):
    '''
    Redis Manager is concerete class which implements the functionality of saving
    and retreiving search keywords mapped to a unique user 
    '''

    STORAGE_TYPE = 'redis'

    async def get_client(self) -> Redis:
        if self._client is None:
            self._client = await aioredis.create_redis_pool(settings.REDIS_URL)

        return self._client

    async def save_recent_search(self, user_id: int, new_search_keyword: str) -> None:
        client = await self.get_client()
        # Using set for uniquness of keywords
        await client.sadd(user_id, new_search_keyword)

    async def get_recent_searches_for_keyword(self, user_id: int, keyword: str) -> List[str]:
        matched_keywords = []
        client = await self.get_client()
        old_searches = await client.smembers(user_id, encoding='utf-8')
        # Simple substr match
        for search in old_searches:
            if keyword in search:
                matched_keywords.append(search)

        return matched_keywords
