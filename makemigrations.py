#!/usr/bin/env python
from django.core.management import call_command

from setup_django import setup_django

setup_django()
call_command("makemigrations", "django_amazon_sns_mobile_push_notification")
