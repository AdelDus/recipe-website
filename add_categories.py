"""
Скрипт для добавления начальных категорий рецептов
Запуск: python manage.py shell < add_categories.py
"""

from game.models import Category

# Список категорий с иконками
categories_data = [
    {'name': 'Горячие блюда', 'icon': '🔥', 'description': 'Горячие основные блюда'},
    {'name': 'Холодные блюда', 'icon': '❄️', 'description': 'Холодные закуски и салаты'},
    {'name': 'Супы', 'icon': '🍲', 'description': 'Первые блюда'},
    {'name': 'Десерты', 'icon': '🍰', 'description': 'Сладкие блюда и выпечка'},
    {'name': 'Напитки', 'icon': '🥤', 'description': 'Напитки и коктейли'},
    {'name': 'Закуски', 'icon': '🥗', 'description': 'Легкие закуски'},
    {'name': 'Выпечка', 'icon': '🥐', 'description': 'Хлеб, булочки, пироги'},
    {'name': 'Салаты', 'icon': '🥙', 'description': 'Овощные и мясные салаты'},
]

# Создаем категории
for cat_data in categories_data:
    category, created = Category.objects.get_or_create(
        name=cat_data['name'],
        defaults={
            'icon': cat_data['icon'],
            'description': cat_data['description']
        }
    )
    if created:
        print(f"✅ Создана категория: {category}")
    else:
        print(f"ℹ️  Категория уже существует: {category}")

print(f"\n📊 Всего категорий: {Category.objects.count()}")
