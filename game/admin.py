from django.contrib import admin
from .models import Recipe, Ingredient, CookingStep


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class CookingStepInline(admin.TabularInline):
    model = CookingStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'cooking_time', 'servings', 'created_at']
    list_filter = ['created_at']
    search_fields = ['title', 'description']
    inlines = [IngredientInline, CookingStepInline]


@admin.register(Ingredient)
class IngredientAdmin(admin.ModelAdmin):
    list_display = ['name', 'recipe', 'quantity', 'unit']
    list_filter = ['recipe']
    search_fields = ['name']


@admin.register(CookingStep)
class CookingStepAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'step_number', 'instruction']
    list_filter = ['recipe']
    ordering = ['recipe', 'step_number']
