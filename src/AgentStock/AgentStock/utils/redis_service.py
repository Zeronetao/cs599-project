import os

import redis

class RedisService:
    def __init__(self, host=None, port=None, password=None, db=None):
        host = host or os.getenv("REDIS_HOST", "localhost")
        port = int(port or os.getenv("REDIS_PORT", "6379"))
        password = password if password is not None else os.getenv("REDIS_PASSWORD")
        db = int(db if db is not None else os.getenv("REDIS_DB", "0"))

        self.r = redis.StrictRedis(
            host=host,
            port=port,
            password=password,
            db=db,
            decode_responses=True  # 自动转为字符串
        )

    # String 类型
    def set_value(self, key, value):
        return self.r.set(key, value)

    def get_value(self, key):
        return self.r.get(key)

    # Hash 类型
    def set_hash(self, key, mapping):
        return self.r.hmset(key, mapping)

    def get_hash(self, key):
        return self.r.hgetall(key)

    # Set 类型
    def add_set(self, key, *values):
        return self.r.sadd(key, *values)

    def get_set(self, key):
        return self.r.smembers(key)

    # SortedSet 类型
    def add_zset(self, key, mapping):
        return self.r.zadd(key, mapping)

    def get_zset(self, key):
        return self.r.zrange(key, 0, -1, withscores=True)

    # List 类型
    def push_list(self, key, *values):
        return self.r.lpush(key, *values)

    def get_list(self, key):
        return self.r.lrange(key, 0, -1)

    # 删除 dev:ops 开头的 key（使用 scan）
    def delete_keys_with_prefix(self, prefix):
        cursor = 0
        while True:
            cursor, keys = self.r.scan(cursor=cursor, match=f"{prefix}*", count=100)
            if keys:
                self.r.delete(*keys)
            if cursor == 0:
                break
