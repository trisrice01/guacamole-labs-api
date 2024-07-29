import redis


class Cache:
    def __init__(self, host):
        self.host = host

    def retrieve_key(self, key: str):
        pass

    def set_key(self, key: str, value: str):
        pass


class RedisCache(Cache):
    def __init__(self, host):
        super().__init__(host)
        self.redis_instance = redis.Redis.from_url(self.host)

    def retrieve_key(self, key: str):
        self.redis_instance.get(key)
        
    def set_key(self, key: str, value: str):
        self.redis_instance.set(key, value)
    