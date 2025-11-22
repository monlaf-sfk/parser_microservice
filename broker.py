import os


from taskiq_aio_pika import AioPikaBroker
from taskiq_redis import RedisAsyncResultBackend

RABBITMQ_URL = os.getenv("RABBITMQ_URL", "amqp://guest:guest@rabbitmq/")
REDIS_URL = os.getenv("REDIS_URL", "redis://redis:6379/0")

result_backend = RedisAsyncResultBackend(redis_url =REDIS_URL)

broker_obj = AioPikaBroker(
    url=RABBITMQ_URL,
    result_backend=result_backend,
)

@broker_obj.on_event("startup")
async def startup():
    print("Broker started!")