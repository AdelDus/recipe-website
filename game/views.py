from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from .models import Recipe, Comment


def home(request):
    """Главная страница со списком рецептов"""
    recipes = Recipe.objects.all()
    return render(request, 'game/home.html', {'recipes': recipes})


def recipe_detail(request, recipe_id):
    """Страница детального просмотра рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    steps = recipe.steps.all()
    comments = recipe.comments.all()
    
    if request.method == 'POST':
        author_name = request.POST.get('author_name', '').strip()
        text = request.POST.get('text', '').strip()
        
        if author_name and text:
            Comment.objects.create(
                recipe=recipe,
                author_name=author_name,
                text=text
            )
            messages.success(request, 'Комментарий успешно добавлен!')
            return redirect('recipe_detail', recipe_id=recipe_id)
        else:
            messages.error(request, 'Пожалуйста, заполните все поля.')
    
    return render(request, 'game/recipe_detail.html', {
        'recipe': recipe,
        'ingredients': ingredients,
        'steps': steps,
        'comments': comments
    })


def like_recipe(request, recipe_id):
    """Добавить лайк рецепту"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.likes += 1
    recipe.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes': recipe.likes})
    return redirect('recipe_detail', recipe_id=recipe_id)


def about(request):
    """Страница о проекте"""
    return render(request, 'game/about.html')