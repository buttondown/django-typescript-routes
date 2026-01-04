import re

import django

from typescript_routes.lib.logic import generate_routes


def test_handles_monkeypatching() -> None:
    # See https://github.com/wrabit/django-cotton/issues/299.

    from django.template import base

    base.tag_re = re.compile(base.tag_re.pattern, re.DOTALL)

    django.setup()

    with open("tests/fixtures/basic.ts") as f:
        assert generate_routes("tests.urls_basic", []) == f.read()
