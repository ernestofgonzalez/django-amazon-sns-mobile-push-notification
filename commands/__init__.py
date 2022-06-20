import sys
from unittest import TestSuite

import click
from django.core.management import call_command


@click.group(invoke_without_command=True)
@click.pass_context
def execute_from_command_line(ctx):
    if ctx.invoked_subcommand is None:
        pass
    else:
        pass


@execute_from_command_line.command()
def makemigrations():
    call_command("makemigrations", "django_amazon_sns_mobile_push_notification")


@execute_from_command_line.command()
def test():
    labels = [
        "tests",
    ]

    from django.test.runner import DiscoverRunner

    runner = DiscoverRunner(verbosity=1)
    failures = runner.run_tests(labels)
    if failures:
        sys.exit(failures)

    return TestSuite()
