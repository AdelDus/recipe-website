@echo off
chcp 65001 >nul
echo ========================================
echo 🍳 Быстрый запуск проекта "Сайт рецептов"
echo ========================================
echo.

echo [1/5] Проверка Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python не найден! Установите Python 3.8+
    pause
    exit /b 1
)
python --version
echo ✅ Python установлен
echo.

echo [2/5] Проверка зависимостей...
pip show django >nul 2>&1
if errorlevel 1 (
    echo 📦 Установка зависимостей...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo ❌ Ошибка установки зависимостей
        pause
        exit /b 1
    )
) else (
    echo ✅ Зависимости установлены
)
echo.

echo [3/5] Проверка базы данных...
if not exist db.sqlite3 (
    echo 🗄️ База данных не найдена. Создание...
    python manage.py migrate
    if errorlevel 1 (
        echo ❌ Ошибка создания базы данных
        pause
        exit /b 1
    )
    
    echo.
    echo 📊 Загрузка демо-данных...
    if exist demo_data.json (
        python manage.py loaddata demo_data.json
        echo ✅ Демо-данные загружены
    ) else (
        echo ⚠️ Файл demo_data.json не найден
        echo 💡 Создайте суперпользователя для доступа к админ-панели:
        echo    python manage.py createsuperuser
    )
) else (
    echo ✅ База данных найдена
    python manage.py migrate --check >nul 2>&1
    if errorlevel 1 (
        echo 🔄 Применение миграций...
        python manage.py migrate
    )
)
echo.

echo [4/5] Проверка медиа-файлов...
if not exist media mkdir media
if not exist media\recipes mkdir media\recipes
echo ✅ Папки для медиа готовы
echo.

echo [5/5] Запуск сервера...
echo.
echo ========================================
echo ✅ Проект готов к работе!
echo ========================================
echo.
echo 🌐 Откройте в браузере: http://127.0.0.1:8000/
echo 👤 Админ-панель: http://127.0.0.1:8000/admin/
echo.
echo 📝 Для остановки сервера нажмите Ctrl+C
echo.
echo ========================================
echo.

python manage.py runserver
