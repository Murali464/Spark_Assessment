from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from django.contrib.auth.models import AbstractUser
import random


def random_int():
    return int(random.randint(10000, 99999))


class UserProfile(AbstractUser):
    username = models.CharField('username', max_length=150, unique=True, default="")
    full_name= models.CharField(max_length=50, default="",blank= False)
    password= models.CharField(max_length=50,blank=False, default="")
    birth_date = models.DateField(null=True, blank=True)
    email = models.EmailField(unique=True, blank=False)
    contact_no = models.IntegerField(unique=True ,null=True)
    Address = models.CharField(max_length=512)
    city = models.CharField(max_length=256)
    country = models.CharField(max_length=256)
    nationality = models.CharField(max_length=256)
    occupation = models.CharField(max_length=256)
    account_no = models.PositiveBigIntegerField(unique=True, default=random_int)
    balance = models.DecimalField(
        default=0,
        max_digits=12,
        decimal_places=2
    )
    USERNAME_FIELD = 'email' # use email to log in
    REQUIRED_FIELDS = ['username']  # required when user is created

    def __str__(self):
        return str(self.username)

    class Meta:
        db_table = "users"


class Transactions(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    amount = models.DecimalField(
        decimal_places=2,
        max_digits=12,
        null=True, blank=True
    )
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.amount)