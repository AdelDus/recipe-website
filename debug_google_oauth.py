#!/usr/bin/env python
"""
Скрипт для отладки Google OAuth redirect URI
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'project.settings')
django.setup()

from django.contrib.sites.models import Site
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.providers.google.provider import GoogleProvider
from django.test import RequestFactory

print("=== ОТЛАДКА GOOGLE OAUTH ===\n")

# Проверяем Site
site = Site.objects.get(id=2)
print(f"1. Текущий Site:")
print(f"   ID: {site.id}")
print(f"   Domain: {site.domain}")
print(f"   Name: {site.name}")

# Проверяем SocialApp
app = SocialApp.objects.get(provider='google')
print(f"\n2. Google OAuth App:")
print(f"   ID: {app.id}")
print(f"   Provider: {app.provider}")
print(f"   Client ID: {app.client_id}")
print(f"   Sites: {[s.domain for s in app.sites.all()]}")

# Проверяем callback URL
print(f"\n3. Ожидаемые Redirect URIs:")
print(f"   http://localhost:8000/accounts/google/login/callback/")
print(f"   http://127.0.0.1:8000/accounts/google/login/callback/")

print(f"\n4. Проверьте в Google Cloud Console:")
print(f"   URL: https://console.cloud.google.com/apis/credentials")
print(f"   Client ID: {app.client_id}")
print(f"\n   В разделе 'Authorized redirect URIs' должны быть:")
print(f"   ✓ http://localhost:8000/accounts/google/login/callback/")
print(f"   ✓ http://127.0.0.1:8000/accounts/google/login/callback/")

print(f"\n5. Authorized JavaScript origins должны быть:")
print(f"   ✓ http://localhost:8000")
print(f"   ✓ http://127.0.0.1:8000")

print(f"\n⚠️  ВАЖНО:")
print(f"   - После изменений в Google Console подождите 1-5 минут")
print(f"   - Очистите кэш браузера или используйте режим инкогнито")
print(f"   - Перезапустите Django сервер")
