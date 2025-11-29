# 🚀 Развертывание проекта на новом ПК

## Предварительные требования

- Python 3.8+
- PostgreSQL (опционально, можно использовать SQLite)
- Git

## Шаг 1: Клонирование репозитория

```bash
git clone <URL_вашего_репозитория>
cd project
```

## Шаг 2: Создание виртуального окружения

```bash
python -m venv venv
venv\Scripts\activate  # Windows
# или
source venv/bin/activate  # Linux/Mac
```

## Шаг 3: Установка зависимостей

```bash
pip install -r requirements.txt
```

## Шаг 4: Настройка переменных окружения

1. Скопируйте `.env.example` в `.env`:
```bash
copy .env.example .env  # Windows
# или
cp .env.example .env  # Linux/Mac
```

2. Отредактируйте `.env` файл:

### Для SQLite (простой вариант):
```env
# Оставьте DB_ENGINE закомментированным или удалите
SECRET_KEY=ваш-секретный-ключ
DEBUG=True

# Google OAuth (если нужен)
GOOGLE_CLIENT_ID=ваш_client_id
GOOGLE_CLIENT_SECRET=ваш_client_secret
```

### Для PostgreSQL:
```env
DB_ENGINE=django.db.backends.postgresql
DB_NAME=recipe_db
DB_USER=postgres
DB_PASSWORD=ваш_пароль
DB_HOST=localhost
DB_PORT=5432

SECRET_KEY=ваш-секретный-ключ
DEBUG=True

GOOGLE_CLIENT_ID=ваш_client_id
GOOGLE_CLIENT_SECRET=ваш_client_secret
```

## Шаг 5: Настройка базы данных

### Вариант A: SQLite (по умолчанию)
```bash
python manage.py migrate
```

### Вариант B: PostgreSQL
1. Создайте базу данных:
```bash
# Запустите PostgreSQL и выполните:
createdb recipe_db
```

2. Запустите миграции:
```bash
python manage.py migrate
```

## Шаг 6: Создание суперпользователя

```bash
python manage.py createsuperuser
```

Введите email и пароль для администратора.

## Шаг 7: Настройка Google OAuth (если нужен)

1. Запустите сервер:
```bash
python manage.py runserver
```

2. Откройте админку: http://127.0.0.1:8000/admin/

3. Войдите с учетными данными суперпользователя

4. **Настройте Site:**
   - Перейдите в "Sites"
   - Измените существующий site или создайте новый:
     - Domain: `127.0.0.1:8000`
     - Display name: `Recipe Website`
   - Запомните ID сайта (обычно 1 или 2)

5. **Обновите SITE_ID в settings.py** (если нужно):
   - Откройте `project/settings.py`
   - Найдите `SITE_ID = 2` и измените на нужный ID

6. **Настройте Social Application:**
   - Перейдите в "Social applications" → "Add"
   - Provider: `Google`
   - Name: `Google OAuth`
   - Client id: ваш Google Client ID
   - Secret key: ваш Google Client Secret
   - Sites: выберите созданный site
   - Сохраните

## Шаг 8: Добавление категорий (опционально)

```bash
python manage.py add_categories
```

## Шаг 9: Запуск сервера

```bash
python manage.py runserver
```

Откройте http://127.0.0.1:8000/

## 🔧 Быстрый старт (SQLite + без Google OAuth)

Если вы хотите быстро запустить проект без PostgreSQL и Google OAuth:

```bash
# 1. Клонировать репозиторий
git clone <URL>
cd project

# 2. Создать виртуальное окружение
python -m venv venv
venv\Scripts\activate

# 3. Установить зависимости
pip install -r requirements.txt

# 4. Создать .env (минимальный)
echo SECRET_KEY=django-insecure-test-key > .env
echo DEBUG=True >> .env

# 5. Миграции
python manage.py migrate

# 6. Создать суперпользователя
python manage.py createsuperuser

# 7. Настроить Site в админке
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.filter(id=1).update(domain='127.0.0.1:8000', name='Recipe Website') or Site.objects.create(id=1, domain='127.0.0.1:8000', name='Recipe Website')"

# 8. Добавить категории
python manage.py add_categories

# 9. Запустить сервер
python manage.py runserver
```

## ⚠️ Важные замечания

### Файлы, которые НЕ попадают в Git:
- `.env` - переменные окружения (секретные ключи)
- `db.sqlite3` - база данных SQLite
- `media/` - загруженные файлы
- `__pycache__/` - кэш Python
- `venv/` - виртуальное окружение

### Что нужно настроить вручную на каждом ПК:
1. ✅ Создать `.env` файл с вашими ключами
2. ✅ Создать базу данных (если PostgreSQL)
3. ✅ Запустить миграции
4. ✅ Создать суперпользователя
5. ✅ Настроить Site в админке
6. ✅ Настроить Google OAuth в админке (если нужен)

### Google OAuth на разных ПК:
- Если оба ПК используют `127.0.0.1:8000` - настройки Google OAuth будут работать
- Если используете разные адреса - нужно добавить их в Google Cloud Console

## 🐛 Решение проблем

### Ошибка "Site matching query does not exist"
```bash
python manage.py shell -c "from django.contrib.sites.models import Site; Site.objects.create(id=2, domain='127.0.0.1:8000', name='Recipe Website')"
```

### Ошибка "redirect_uri_mismatch" (Google OAuth)
1. Проверьте, что в Google Cloud Console добавлены redirect URIs:
   - `http://127.0.0.1:8000/accounts/google/login/callback/`
   - `http://localhost:8000/accounts/google/login/callback/`
2. Проверьте SITE_ID в settings.py

### База данных не создается (PostgreSQL)
```bash
# Проверьте, что PostgreSQL запущен
# Создайте базу вручную:
psql -U postgres
CREATE DATABASE recipe_db;
\q
```

## 📚 Дополнительная информация

- [GOOGLE_AUTH_SETUP.md](GOOGLE_AUTH_SETUP.md) - подробная настройка Google OAuth
- [БИЗНЕС_ЛОГИКА.md](БИЗНЕС_ЛОГИКА.md) - описание функционала
- [БЫСТРЫЙ_СТАРТ.md](БЫСТРЫЙ_СТАРТ.md) - быстрый старт проекта
