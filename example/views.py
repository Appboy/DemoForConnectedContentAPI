import os
import random

import redis
from django.http import HttpResponse

r = redis.from_url(os.environ.get("REDIS_URL"))


def index_view(request):
    model_id = random.randint(0, 20_000)
    # obj = MyModel.objects.get(id=model_id)
    value = r.get("user:{}".format(model_id))
    return HttpResponse(value)
