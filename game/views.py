from django.shortcuts import render, get_object_or_404
from .models import Recipe


def home(request):
    """Главная страница со списком рецептов"""
    recipes = Recipe.objects.all()
    return render(request, 'game/home.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    """Страница детального просмотра рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    steps = recipe.steps.all()
    return render(request, 'game/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'steps': steps
    })


def about(request):
    """Страница о проекте"""
    return render(request, 'game/about.html')