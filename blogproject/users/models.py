from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    nickname = models.CharField(max_length=32, verbose_name='昵称')

    class Meta(AbstractUser.Meta):
        pass

    def __str__(self):
        return self.nickname
