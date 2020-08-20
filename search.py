from typing import List, Optional

import aiohttp

from settings import settings


class GoogleSearch:
    '''
    Class to handle the google search and extracting the useful data from API response
    '''
    API_ENDPOINT = 'https://www.googleapis.com/customsearch/v1'

    async def _search(self, query: str, *, max_count: Optional[int] = None) -> List:
        '''
        To make an API call and return the results
        '''
        async with self._session.get(
            self.API_ENDPOINT,
            params={
                'key': settings.GOOGLE_API_KEY,
                'cx': settings.GOOGLE_SEARCH_ENGINE_KEY,
                'q': query,
            },
        ) as response:
            response.status
            search_result = await response.json()

        if max_count:
            return search_result['items'][:max_count]
        return search_result['items']

    # aiohttp uses session pool so we are just keeping one session for the whole application 
    async def __aenter__(self):
        self._session = aiohttp.ClientSession()
        return self

    async def __aexit__(self, *err):
        await self._session.close()
        self._session = None

    async def get_top_5_links(self, query: str) -> List[str]:
        '''
        This method fetches the top 5 links from google search for a given query
        '''
        links = []
        results = await self._search(query, max_count=5)
        for result in results:
            links.append(result['link'])
        return links
