from django.db import models


class MyModel(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.CharField(max_length=140)
