from django.urls import get_resolver
from typescript_routes.lib.logic import extract_routes, generate_routes

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

    expectation = open("tests/fixtures/basic.ts").read()
    reality = generate_routes("tests.urls_basic", [])
    assert reality == expectation, f"Expected:\n{expectation}\n\nGot:\n{reality}"
