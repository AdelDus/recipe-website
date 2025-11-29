from django.contrib import admin
from .models import Category, Recipe, Ingredient, CookingStep, Comment, Favorite


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'icon', 'recipe_count', 'created_at']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at']

    def recipe_count(self, obj):
        return obj.recipes.count()
    recipe_count.short_description = 'Количество рецептов'


class IngredientInline(admin.TabularInline):
    model = Ingredient
    extra = 1


class CookingStepInline(admin.TabularInline):
    model = CookingStep
    extra = 1


@admin.register(Recipe)
class RecipeAdmin(admin.ModelAdmin):
    list_display = ['title', 'author_name', 'category', 'is_approved', 'cooking_time', 'servings', 'likes', 'created_at']
    list_filter = ['is_approved', 'category', 'created_at']
    search_fields = ['title', 'description', 'author_name']
    readonly_fields = ['likes', 'created_at', 'updated_at']
    inlines = [IngredientInline, CookingStepInline]
    actions = ['approve_recipes', 'reject_recipes']
    
    def approve_recipes(self, request, queryset):
        updated = queryset.update(is_approved=True)
        self.message_user(request, f'{updated} рецептов одобрено.')
    approve_recipes.short_description = 'Одобрить выбранные рецепты'
    
    def reject_recipes(self, request, queryset):
        updated = queryset.update(is_approved=False)
        self.message_user(request, f'{updated} рецептов отклонено.')
    reject_recipes.short_description = 'Отклонить выбранные рецепты'


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


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['author_name', 'recipe', 'text', 'created_at']
    list_filter = ['created_at', 'recipe']
    search_fields = ['author_name', 'text']
    readonly_fields = ['created_at']


@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ['recipe', 'session_key', 'created_at']
    list_filter = ['created_at', 'recipe']
    search_fields = ['recipe__title', 'session_key']
    readonly_fields = ['created_at']
