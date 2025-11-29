from django.db import models


class Recipe(models.Model):
    """Модель рецепта"""
    title = models.CharField(max_length=200, verbose_name='Название')
    description = models.TextField(verbose_name='Описание')
    cooking_time = models.IntegerField(verbose_name='Время приготовления (мин)')
    servings = models.IntegerField(default=1, verbose_name='Количество порций')
    image = models.ImageField(upload_to='recipes/', verbose_name='Изображение блюда')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ['-created_at']

    def __str__(self):
        return self.title


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
