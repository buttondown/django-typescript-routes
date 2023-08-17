from django.urls import get_resolver
from typescript_routes.lib.logic import extract_routes, generate_routes
from django.urls import path


def test_extract_routes_smoke() -> None:
    resolver = get_resolver("tests.urls")
    assert list(extract_routes(resolver, [])) == []

def test_generate_routes_smoke() -> None:
    import django
    django.setup()

    assert generate_routes("tests.urls", []) == open("tests/fixtures/empty.ts").read()


def test_generate_routes_basic() -> None:
    import django
    django.setup()

    assert generate_routes("tests.urls_basic", []) == open("tests/fixtures/basic.ts").read()
