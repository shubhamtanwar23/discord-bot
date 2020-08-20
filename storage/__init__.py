from storage.exceptions import StorageManagerNotFound



class StorageManager:
    '''
    This is an interface for storing/retreival of search keywords
    This should be extended to add storage types like Databse, Redis, File etc
    '''
    _client = None
    TYPE = None

    async def get_client(self):
        '''
        A coroutine which handles the connection setup
        '''
        ...

    async def save_recent_search(self, user_id: int, new_search_keyword: str) -> None:
        '''
        A coroutine which handles savings the new search keyword repective to user
        '''
        ...

    async def get_recent_searches_for_keyword(self, user_id: int, keyword: str) -> str:
        '''
        A coroutine which handles retreiving of old search keywords partially matching
        to the given keyword
        '''
        ...


STORAGE_MANAGERS = None


def _init_storage_clients():
    def get_all_subclasses(cls):
        all_subclasses = []

        for subclass in cls.__subclasses__():
            all_subclasses.append(subclass)
            all_subclasses.extend(get_all_subclasses(subclass))

        return all_subclasses

    from storage.redis import RedisManager

    global STORAGE_MANAGERS
    STORAGE_MANAGERS = {
        c.STORAGE_TYPE.lower(): c
        for c in get_all_subclasses(StorageManager)
        if c.STORAGE_TYPE is not None
    }


def get_storage_manager(storage_type: str) -> StorageManager:
    '''
    Helper method to get the respective StorageManager instance as per storage type
    For example:
    'redis':- This will give RedisManager instance
    '''
    global STORAGE_MANAGERS
    if STORAGE_MANAGERS is None:
        _init_storage_clients()
    try:
        return STORAGE_MANAGERS[storage_type.lower()]()
    except KeyError:
        raise StorageManagerNotFound(f'Storage Manager for type {storage_type} is not supported')
