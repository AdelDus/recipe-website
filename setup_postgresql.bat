@echo off
chcp 65001 >nul
echo ========================================
echo 🐘 Настройка PostgreSQL для защиты
echo ========================================
echo.

echo Этот скрипт поможет настроить PostgreSQL на компьютере преподавателя.
echo.
echo ТРЕБОВАНИЯ:
echo 1. PostgreSQL должен быть установлен
echo 2. Вы должны знать пароль пользователя postgres
echo.
pause

echo.
echo [1/6] Проверка PostgreSQL...
psql --version >nul 2>&1
if errorlevel 1 (
    echo ❌ PostgreSQL не найден!
    echo.
    echo Установите PostgreSQL:
    echo https://www.postgresql.org/download/windows/
    echo.
    echo После установки запустите этот скрипт снова.
    pause
    exit /b 1
)
psql --version
echo ✅ PostgreSQL установлен
echo.

echo [2/6] Проверка Python зависимостей...
pip show psycopg2 >nul 2>&1
if errorlevel 1 (
    echo 📦 Установка psycopg2...
    pip install psycopg2
)
pip show python-decouple >nul 2>&1
if errorlevel 1 (
    echo 📦 Установка python-decouple...
    pip install python-decouple
)
echo ✅ Зависимости установлены
echo.

echo [3/6] Создание базы данных...
echo.
echo Введите пароль пользователя postgres:
set /p POSTGRES_PASSWORD=Пароль: 

echo.
echo Создание базы данных recipe_db...
set PGPASSWORD=%POSTGRES_PASSWORD%
psql -U postgres -c "DROP DATABASE IF EXISTS recipe_db;" 2>nul
psql -U postgres -c "CREATE DATABASE recipe_db;"
if errorlevel 1 (
    echo ❌ Ошибка создания базы данных
    echo Проверьте пароль и попробуйте снова
    pause
    exit /b 1
)
echo ✅ База данных recipe_db создана
echo.

echo [4/6] Создание файла .env...
(
echo # Database Configuration
echo DB_ENGINE=django.db.backends.postgresql
echo DB_NAME=recipe_db
echo DB_USER=postgres
echo DB_PASSWORD=%POSTGRES_PASSWORD%
echo DB_HOST=localhost
echo DB_PORT=5432
echo.
echo # Django Secret Key
echo SECRET_KEY=django-insecure-#qw(!$*zt!#xn%)0x(02()lu_&9w848!(4=^liy^_n^p$8(k2q
echo.
echo # Debug Mode
echo DEBUG=True
) > .env
echo ✅ Файл .env создан
echo.

echo [5/6] Применение миграций...
python manage.py migrate
if errorlevel 1 (
    echo ❌ Ошибка применения миграций
    pause
    exit /b 1
)
echo ✅ Миграции применены
echo.

echo [6/6] Загрузка демо-данных...
if exist demo_data.json (
    python manage.py loaddata demo_data.json
    if errorlevel 1 (
        echo ⚠️ Ошибка загрузки демо-данных
        echo Продолжаем без демо-данных...
    ) else (
        echo ✅ Демо-данные загружены
    )
) else (
    echo ⚠️ Файл demo_data.json не найден
    echo.
    echo Создайте суперпользователя:
    echo python manage.py createsuperuser
)
echo.

echo ========================================
echo ✅ PostgreSQL настроен!
echo ========================================
echo.
echo База данных: recipe_db
echo Пользователь: postgres
echo Хост: localhost
echo Порт: 5432
echo.
echo Запуск сервера...
echo.
python manage.py runserver
