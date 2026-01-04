# Changelog

## 0.4.0

- Added support for Django 6.0.
- Bumped minimum Python version to 3.12 (required by Django 6.0).
- Fixed syntax warnings in tests for Python 3.12+.
- Cleaned up resource leaks in test suite.

## 0.3.0

- Migrated from `poetry` to `uv`.
- Refactored the template to be amenable to packages that monkey-patch the template engine.
