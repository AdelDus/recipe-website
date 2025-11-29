@echo off
chcp 65001 >nul
echo ========================================
echo 📤 Экспорт базы данных PostgreSQL
echo ========================================
echo.

echo Этот скрипт создаст SQL дамп базы данных для переноса на другой компьютер.
echo.

if not exist .env (
    echo ❌ Файл .env не найден!
    echo Убедитесь, что вы используете PostgreSQL.
    pause
    exit /b 1
)

echo Введите пароль пользователя postgres:
set /p POSTGRES_PASSWORD=Пароль: 

echo.
echo Создание SQL дампа...
set PGPASSWORD=%POSTGRES_PASSWORD%
pg_dump -U postgres recipe_db > recipe_db_dump.sql

if errorlevel 1 (
    echo ❌ Ошибка создания дампа
    echo Проверьте:
    echo - PostgreSQL установлен
    echo - База данных recipe_db существует
    echo - Пароль правильный
    pause
    exit /b 1
)

echo ✅ SQL дамп создан: recipe_db_dump.sql
echo.

echo Также создаем JSON дамп для совместимости...
python manage.py dumpdata game --indent 4 > demo_data.json

if errorlevel 1 (
    echo ⚠️ Ошибка создания JSON дампа
) else (
    echo ✅ JSON дамп создан: demo_data.json
)

echo.
echo ========================================
echo ✅ Экспорт завершен!
echo ========================================
echo.
echo Созданные файлы:
echo - recipe_db_dump.sql (SQL дамп PostgreSQL)
echo - demo_data.json (JSON дамп Django)
echo.
echo Закоммитьте эти файлы в Git:
echo    git add recipe_db_dump.sql demo_data.json
echo    git commit -m "Add database dumps"
echo    git push
echo.
pause
