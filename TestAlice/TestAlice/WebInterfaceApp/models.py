from django.db import models
from django.utils import timezone


class UserRequest(models.Model):
    user_id = models.CharField(verbose_name='User ID', max_length=100, null=False)
    session_id = models.CharField(verbose_name='Session ID', max_length=100, null=False)
    request_datetime = models.DateTimeField(verbose_name='Request time', default=timezone.now)
    command = models.TextField(verbose_name='Command text')
