from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    """Модель категории рецепта"""
    name = models.CharField(max_length=100, unique=True, verbose_name='Название')
    description = models.TextField(blank=True, verbose_name='Описание')
    icon = models.CharField(max_length=10, default='🍽️', verbose_name='Иконка')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
        ordering = ['name']

    def __str__(self):
        return f"{self.icon} {self.name}"


class Recipe(models.Model):
    """Модель рецепта"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True, related_name='recipes', verbose_name='Категория')
    cooking_time = models.IntegerField(verbose_name='Время приготовления (мин)')
    servings = models.IntegerField(default=1, verbose_name='Количество порций')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение блюда')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='recipes', verbose_name='Автор', null=True)
    author_name = models.CharField(max_length=100, default='Аноним', verbose_name='Имя автора')
    is_approved = models.BooleanField(default=False, verbose_name='Одобрен')
    likes = models.IntegerField(default=0, verbose_name='Лайки')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def clean(self):
        """Валидация бизнес-правил"""
        from django.core.exceptions import ValidationError
        
        if self.cooking_time <= 0:
            raise ValidationError({'cooking_time': 'Время приготовления должно быть больше 0 минут'})
        
        if self.cooking_time > 1440:  # 24 часа
            raise ValidationError({'cooking_time': 'Время приготовления не может превышать 24 часа (1440 минут)'})
        
        if self.servings <= 0:
            raise ValidationError({'servings': 'Количество порций должно быть больше 0'})
        
        if self.servings > 100:
            raise ValidationError({'servings': 'Количество порций не может превышать 100'})
        
        if self.likes < 0:
            self.likes = 0  # Автоматическая коррекция

    @property
    def comment_count(self):
        """Количество комментариев"""
        return self.comments.count()

    @property
    def has_ingredients(self):
        """Проверка наличия ингредиентов"""
        return self.ingredients.exists()

    @property
    def has_steps(self):
        """Проверка наличия шагов"""
        return self.steps.exists()

    @property
    def is_complete(self):
        """Проверка полноты рецепта"""
        return self.has_ingredients and self.has_steps


class Ingredient(models.Model):
    """Модель ингредиента"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='ingredients', verbose_name='Рецепт')
    name = models.CharField(max_length=200, verbose_name='Название')
    quantity = models.CharField(max_length=50, verbose_name='Количество')
    unit = models.CharField(max_length=50, verbose_name='Единица измерения')

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return f"{self.name} - {self.quantity} {self.unit}"


class CookingStep(models.Model):
    """Модель шага приготовления"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='steps', verbose_name='Рецепт')
    step_number = models.IntegerField(verbose_name='Номер шага')
    instruction = models.TextField(verbose_name='Инструкция')

    class Meta:
        verbose_name = 'Шаг приготовления'
        verbose_name_plural = 'Шаги приготовления'
        ordering = ['step_number']

    def __str__(self):
        return f"Шаг {self.step_number} - {self.recipe.title}"


class Comment(models.Model):
    """Модель комментария"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='comments', verbose_name='Рецепт')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comments', verbose_name='Автор', null=True)
    author_name = models.CharField(max_length=100, verbose_name='Имя автора')
    text = models.TextField(verbose_name='Текст комментария')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.author_name} - {self.recipe.title}"


class Favorite(models.Model):
    """Модель избранного (для анонимных пользователей через сессию)"""
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE, related_name='favorites', verbose_name='Рецепт')
    session_key = models.CharField(max_length=40, verbose_name='Ключ сессии')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранное'
        unique_together = ['recipe', 'session_key']
        ordering = ['-created_at']

    def __str__(self):
        return f"{self.recipe.title} - {self.session_key[:8]}..."
