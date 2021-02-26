from django.db import models
from django.contrib.auth.models import User


class Manager(models.Model):
    name = models.CharField(max_length=20)
    mobile_no = models.IntegerField()
    email = models.EmailField()
    password = models.CharField(max_length=10)

    def __str__(self):
        return self.name


