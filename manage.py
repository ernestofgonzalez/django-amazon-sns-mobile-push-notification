#!/usr/bin/env python
"""Command-line utility for administrative tasks."""
import os

import django
from django.conf import settings


def main():
    """Run administrative tasks"""
    from commands import execute_from_command_line

    BASE_DIR = os.path.abspath(
        os.path.join(
            os.path.dirname(__file__), "django_amazon_sns_mobile_push_notification"
        )
    )

    settings.configure(
        BASE_DIR=BASE_DIR,
        DEBUG=True,
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
                "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
            }
        },
        INSTALLED_APPS=("django_amazon_sns_mobile_push_notification",),
        TIME_ZONE="UTC",
        USE_TZ=True,
    )

    django.setup()

    execute_from_command_line()


if __name__ == "__main__":
    main()
