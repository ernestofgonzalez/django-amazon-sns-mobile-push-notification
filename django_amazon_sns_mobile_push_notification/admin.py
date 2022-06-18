from django.contrib import admin

from django_amazon_sns_mobile_push_notification.models import Device, Log

admin.site.register(Device)
admin.site.register(Log)
