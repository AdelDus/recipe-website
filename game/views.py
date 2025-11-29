from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.contrib import messages
from django.db.models import Q
from .models import Category, Recipe, Comment, Favorite


def home(request):
    """Главная страница со списком рецептов"""
    category_id = request.GET.get('category')
    search_query = request.GET.get('q', '').strip()
    categories = Category.objects.all()
    
    # Базовый queryset - только одобренные рецепты
    recipes = Recipe.objects.filter(is_approved=True)
    
    # Фильтрация по категории
    if category_id:
        recipes = recipes.filter(category_id=category_id)
        selected_category = get_object_or_404(Category, id=category_id)
    else:
        selected_category = None
    
    # Поиск
    if search_query:
        recipes = recipes.filter(
            Q(title__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(ingredients__name__icontains=search_query)
        ).distinct()
    
    # Получаем избранные рецепты для текущей сессии
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    favorite_ids = Favorite.objects.filter(session_key=session_key).values_list('recipe_id', flat=True)
    
    return render(request, 'game/home.html', {
        'recipes': recipes,
        'categories': categories,
        'selected_category': selected_category,
        'search_query': search_query,
        'favorite_ids': list(favorite_ids)
    })


def recipe_detail(request, recipe_id):
    """Страница детального просмотра рецепта"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    ingredients = recipe.ingredients.all()
    steps = recipe.steps.all()
    comments = recipe.comments.all()
    
    # Проверяем, в избранном ли рецепт
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    is_favorite = Favorite.objects.filter(recipe=recipe, session_key=session_key).exists()
    
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
        'comments': comments,
        'is_favorite': is_favorite
    })


def like_recipe(request, recipe_id):
    """Добавить лайк рецепту"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    recipe.likes += 1
    recipe.save()
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'likes': recipe.likes})
    return redirect('recipe_detail', recipe_id=recipe_id)


def toggle_favorite(request, recipe_id):
    """Добавить/удалить рецепт из избранного"""
    recipe = get_object_or_404(Recipe, id=recipe_id)
    
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    favorite, created = Favorite.objects.get_or_create(
        recipe=recipe,
        session_key=session_key
    )
    
    if not created:
        favorite.delete()
        is_favorite = False
        message = 'Рецепт удален из избранного'
    else:
        is_favorite = True
        message = 'Рецепт добавлен в избранное'
    
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({'is_favorite': is_favorite, 'message': message})
    
    messages.success(request, message)
    return redirect('recipe_detail', recipe_id=recipe_id)


def favorites(request):
    """Страница избранных рецептов"""
    if not request.session.session_key:
        request.session.create()
    session_key = request.session.session_key
    
    favorite_recipes = Recipe.objects.filter(
        favorites__session_key=session_key
    ).order_by('-favorites__created_at')
    
    return render(request, 'game/favorites.html', {
        'recipes': favorite_recipes
    })


def add_recipe(request):
    """Страница добавления рецепта"""
    from .forms import RecipeForm, IngredientFormSet, CookingStepFormSet
    
    if request.method == 'POST':
        recipe_form = RecipeForm(request.POST, request.FILES)
        
        if recipe_form.is_valid():
            recipe = recipe_form.save(commit=False)
            recipe.is_approved = False  # Требует модерации
            recipe.save()
            
            # Сохраняем ингредиенты
            ingredient_formset = IngredientFormSet(request.POST, instance=recipe)
            if ingredient_formset.is_valid():
                ingredient_formset.save()
            
            # Сохраняем шаги
            step_formset = CookingStepFormSet(request.POST, instance=recipe)
            if step_formset.is_valid():
                step_formset.save()
            
            messages.success(request, 'Рецепт отправлен на модерацию! После проверки он появится на сайте.')
            return redirect('home')
        else:
            messages.error(request, 'Пожалуйста, исправьте ошибки в форме.')
            ingredient_formset = IngredientFormSet(request.POST)
            step_formset = CookingStepFormSet(request.POST)
    else:
        recipe_form = RecipeForm()
        ingredient_formset = IngredientFormSet()
        step_formset = CookingStepFormSet()
    
    return render(request, 'game/add_recipe.html', {
        'recipe_form': recipe_form,
        'ingredient_formset': ingredient_formset,
        'step_formset': step_formset
    })


def about(request):
    """Страница о проекте"""
    return render(request, 'game/about.html')