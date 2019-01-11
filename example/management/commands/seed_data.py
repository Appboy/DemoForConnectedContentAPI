import random
import string

from django.core.management.base import BaseCommand

from example.models import MyModel


class Command(BaseCommand):
    help = 'Creates 20k pieces of test data'

    def handle(self, *args, **kwargs):
        for i in range(20_000):
            value = ''.join(random.choices(string.ascii_uppercase + string.digits, k=140))
            MyModel.objects.create(value=value)
