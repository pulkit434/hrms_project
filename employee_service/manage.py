#!/usr/bin/env python
import os
import sys

def main():
    print("Starting manage.py...")  # debug print
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'employee_service.settings')
    print("DJANGO_SETTINGS_MODULE set")  # debug print

    try:
        import django
        print("Django imported successfully")  # debug print
        from django.core.management import execute_from_command_line
        print("execute_from_command_line imported")  # debug print
    except ImportError as exc:
        print("ImportError:", exc)
        raise

    print("Running command:", sys.argv)
    execute_from_command_line(sys.argv)

if __name__ == '__main__':
    main()
