from celery import Celery
import os
from dotenv import load_dotenv

load_dotenv()

app = Celery(
    'tasks',
    broker=os.getenv("REDIS_BROKER_URL"),
    backend=os.getenv("REDIS_BROKER_URL")
)

app.conf.timezone = 'UTC'

import worker.tasks

app.conf.beat_schedule = {
    'collect_rankings_every_2_minutes': {
        'task': 'worker.tasks.collect_and_merge_data',
        'schedule': 120.0,
    },
}