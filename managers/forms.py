from django.db import models
from accounts.models import UserProfile
from managers.models import Manager
import datetime
from django import forms


class ManagerForm(forms.ModelForm):

    class Meta:
        model = Manager
        fields = "__all__"


