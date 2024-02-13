#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

os.chdir(BASE_DIR)
sys.path.insert(0, BASE_DIR)


def main():
    """Run administrative tasks."""
    try:
        import wallet_wise.settings_local
    except ModuleNotFoundError:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_wise.settings")
    else:
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "wallet_wise.settings_local")
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == "__main__":
    main()
