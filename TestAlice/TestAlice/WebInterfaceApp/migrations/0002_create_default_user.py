# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations
from django.contrib.auth.models import User


def add_default_user(apps, schema_editor):
    from django.db import transaction
    with transaction.atomic():
        user = User(username='user', email='user@example.com')
        user.set_password('user')
        user.save()


class Migration(migrations.Migration):

    dependencies = [
        ('WebInterfaceApp', '0001_initial'),
    ]

    operations = [
        migrations.RunPython(
            add_default_user)
    ]