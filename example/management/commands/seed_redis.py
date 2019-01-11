import os
import random
import string

import redis
from django.core.management.base import BaseCommand

from example.models import MyModel


class Command(BaseCommand):
    help = 'Load test data into Redis'

    def handle(self, *args, **kwargs):
        r = redis.from_url(os.environ.get("REDIS_URL"))
        for i in range(1, 20_000):
            m = MyModel.objects.get(id=i)
            r.set("user:{}".format(m.id), m.value)

        print("Done!")
