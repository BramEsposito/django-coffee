#!/usr/bin/env python
"""
Test runner script for django-coffee-admin

Usage:
    python runtests.py              # Run all tests
    python runtests.py -v           # Verbose output
    python runtests.py -k test_name # Run specific test
    python runtests.py --cov        # Run with coverage report
"""
import sys
import pytest


def main():
    """Run pytest with default arguments"""
    args = sys.argv[1:]

    # Default pytest arguments
    default_args = [
        'tests/',
        '--verbose',
    ]

    # Combine default args with user args
    pytest_args = args if args else default_args

    # Run pytest
    exit_code = pytest.main(pytest_args)

    return exit_code


if __name__ == '__main__':
    sys.exit(main())
