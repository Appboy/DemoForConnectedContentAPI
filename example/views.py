import random

from django.http import HttpResponse

from example.models import MyModel


def index_view(request):
    model_id = random.randint(0, 20_000)
    obj = MyModel.objects.get(id=model_id)
    return HttpResponse(obj.value)
