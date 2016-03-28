#!/usr/bin/env python
import os
import sys


def main():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(sys.argv)


def test():
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "test_project.settings")
    from django.core.management import execute_from_command_line
    execute_from_command_line(['test', 'flickr_pony'])

if __name__ == "__main__":
    main()
