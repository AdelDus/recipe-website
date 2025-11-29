#!/usr/bin/env python
"""
Скрипт для исправления проблемы с дублированием Google OAuth приложений
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from allauth.socialaccount.models import SocialApp
from django.contrib.sites.models import Site
from decouple import config

# Удаляем все Google OAuth приложения
print("Удаление существующих Google OAuth приложений...")
deleted_count = SocialApp.objects.filter(provider='google').delete()[0]
print(f"Удалено приложений: {deleted_count}")

# Получаем текущий сайт
site = Site.objects.get(id=2)
print(f"Используется сайт: {site.domain}")

# Создаем новое приложение
print("Создание нового Google OAuth приложения...")
google_app = SocialApp.objects.create(
    provider='google',
    name='Google OAuth',
    client_id=config('GOOGLE_CLIENT_ID', default=''),
    secret=config('GOOGLE_CLIENT_SECRET', default=''),
)
google_app.sites.add(site)
print(f"Создано приложение ID: {google_app.id}")

print("\nГотово! Теперь перезапустите сервер.")
