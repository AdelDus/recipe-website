#!/usr/bin/env python
"""
Скрипт для проверки конфигурации Google OAuth
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site

print("=== ПРОВЕРКА САЙТОВ ===")
sites = Site.objects.all()
print(f"Всего сайтов: {sites.count()}")
for site in sites:
    print(f"  ID: {site.id}, Domain: {site.domain}, Name: {site.name}")

print("\n=== ПРОВЕРКА SOCIAL APPS ===")
apps = SocialApp.objects.all()
print(f"Всего приложений: {apps.count()}")
for app in apps:
    print(f"  ID: {app.id}, Provider: {app.provider}, Name: {app.name}")
    print(f"  Client ID: {app.client_id[:30]}...")
    print(f"  Связано с сайтами: {[s.id for s in app.sites.all()]}")

print("\n=== ПРОВЕРКА GOOGLE APPS ===")
google_apps = SocialApp.objects.filter(provider='google')
print(f"Google приложений: {google_apps.count()}")
for app in google_apps:
    print(f"  ID: {app.id}, Name: {app.name}")
    sites_list = list(app.sites.all())
    print(f"  Сайты: {[(s.id, s.domain) for s in sites_list]}")

# Проверка через raw SQL
from django.db import connection
print("\n=== ПРОВЕРКА ЧЕРЕЗ SQL ===")
with connection.cursor() as cursor:
    cursor.execute("SELECT id, provider, name, client_id FROM socialaccount_socialapp WHERE provider='google'")
    rows = cursor.fetchall()
    print(f"Записей в БД: {len(rows)}")
    for row in rows:
        print(f"  {row}")
    
    cursor.execute("SELECT * FROM socialaccount_socialapp_sites WHERE socialapp_id IN (SELECT id FROM socialaccount_socialapp WHERE provider='google')")
    rows = cursor.fetchall()
    print(f"\nСвязей app-site: {len(rows)}")
    for row in rows:
        print(f"  {row}")
