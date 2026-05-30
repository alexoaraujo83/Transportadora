#!/usr/bin/env bash
set -euo pipefail
python manage.py check --settings=config.test_settings
python manage.py makemigrations --check --dry-run --settings=config.test_settings
python manage.py migrate --settings=config.test_settings
python manage.py test --settings=config.test_settings
python manage.py gerar_insights --settings=config.test_settings || true
