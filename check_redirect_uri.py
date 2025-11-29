#!/usr/bin/env python
"""
Скрипт для проверки правильного redirect URI для Google OAuth
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp

print("=== ПРОВЕРКА REDIRECT URI ===\n")

# Получаем текущий сайт
site = Site.objects.get(id=2)
print(f"Текущий сайт: {site.domain}")
print(f"Протокол: http (для разработки)")

# Формируем правильный redirect URI
redirect_uri = f"http://{site.domain}/accounts/google/login/callback/"
print(f"\n✅ ПРАВИЛЬНЫЙ REDIRECT URI для Google Cloud Console:")
print(f"   {redirect_uri}")

print("\n📋 ЧТО НУЖНО СДЕЛАТЬ:")
print("1. Откройте Google Cloud Console: https://console.cloud.google.com/")
print("2. Перейдите в 'APIs & Services' → 'Credentials'")
print("3. Найдите ваш OAuth 2.0 Client ID и нажмите на него")
print("4. В разделе 'Authorized redirect URIs' добавьте:")
print(f"   {redirect_uri}")
print("5. Нажмите 'SAVE'")
print("6. Подождите 1-2 минуты для применения изменений")
print("7. Перезапустите Django сервер")

# Проверяем настройки приложения
try:
    app = SocialApp.objects.get(provider='google')
    print(f"\n✅ Google OAuth приложение настроено:")
    print(f"   Client ID: {app.client_id[:30]}...")
    print(f"   Связано с сайтом: {site.domain}")
except SocialApp.DoesNotExist:
    print("\n❌ Google OAuth приложение НЕ настроено в админке!")
    print("   Зайдите в /admin/ и настройте Social Application")
