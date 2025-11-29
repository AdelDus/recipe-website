#!/usr/bin/env python
"""
Скрипт для переключения Site на 127.0.0.1 вместо localhost
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.sites.models import Site

site = Site.objects.get(id=2)
print(f"Текущий domain: {site.domain}")

site.domain = '127.0.0.1:8000'
site.name = 'Recipe Website'
site.save()

print(f"Новый domain: {site.domain}")
print("\nТеперь перезапустите сервер и попробуйте войти через:")
print("http://127.0.0.1:8000/accounts/login/")
