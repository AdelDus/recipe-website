from django.core.management.base import BaseCommand
from game.models import Category


class Command(BaseCommand):
    help = 'Добавляет начальные категории рецептов'

    def handle(self, *args, **options):
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

        created_count = 0
        existing_count = 0

        for cat_data in categories_data:
            category, created = Category.objects.get_or_create(
                name=cat_data['name'],
                defaults={
                    'icon': cat_data['icon'],
                    'description': cat_data['description']
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f'✅ Создана категория: {category}'))
                created_count += 1
            else:
                self.stdout.write(self.style.WARNING(f'ℹ️  Категория уже существует: {category}'))
                existing_count += 1

        self.stdout.write(self.style.SUCCESS(f'\n📊 Создано новых категорий: {created_count}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Уже существовало: {existing_count}'))
        self.stdout.write(self.style.SUCCESS(f'📊 Всего категорий: {Category.objects.count()}'))
