@echo off
echo ========================================
echo Переключение на PostgreSQL
echo ========================================
echo.

if not exist .env (
    echo Создание файла .env...
    copy .env.example .env
    echo.
    echo ВАЖНО: Отредактируйте файл .env и укажите:
    echo - DB_PASSWORD (пароль PostgreSQL)
    echo - DB_NAME (имя базы данных)
    echo - DB_USER (пользователь PostgreSQL)
    echo.
    echo После редактирования запустите скрипт снова.
    pause
    exit /b
)

echo Проверка подключения к PostgreSQL...
python -c "import psycopg2; print('psycopg2 установлен')" 2>nul
if errorlevel 1 (
    echo Ошибка: psycopg2 не установлен
    echo Установка psycopg2...
    pip install psycopg2
)

echo.
echo Применение миграций...
python manage.py migrate

echo.
echo ========================================
echo Готово! Проект использует PostgreSQL
echo ========================================
echo.
echo Для создания суперпользователя выполните:
echo python manage.py createsuperuser
echo.
pause
