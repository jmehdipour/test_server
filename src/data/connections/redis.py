import redis

from config import get_settings

connection_pool = None


def get_redis_connection(server_name='default'):
    '''
    Gets the specified redis connection
    '''
    global connection_pool

    if connection_pool is None:
        connection_pool = setup_redis()

    pool = connection_pool[server_name]

    return redis.StrictRedis(connection_pool=pool)


def setup_redis():
    '''
    Starts the connection pool for all configured redis servers
    '''
    pools = {}

    pool = redis.ConnectionPool.from_url(get_settings().redis_url,
                                         decode_responses=True,
                                         socket_timeout=None,
                                         socket_connect_timeout=None,
                                         socket_keepalive=False,
                                         socket_keepalive_options=None,
                                         retry_on_timeout=True,
                                         max_connections=10,
                                         health_check_interval=50
                                         )
    pools['default'] = pool
    return pools
