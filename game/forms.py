from django import forms
from .models import Recipe, Ingredient, CookingStep


class RecipeForm(forms.ModelForm):
    """Форма для создания рецепта"""
    
    class Meta:
        model = Recipe
        fields = ['title', 'description', 'category', 'cooking_time', 'servings', 'image', 'author_name']
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Например: Борщ украинский'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите ваш рецепт...',
                'rows': 4
            }),
            'category': forms.Select(attrs={'class': 'form-control'}),
            'cooking_time': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'В минутах',
                'min': 1
            }),
            'servings': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество порций',
                'min': 1
            }),
            'image': forms.FileInput(attrs={'class': 'form-control'}),
            'author_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Ваше имя'
            }),
        }


class IngredientForm(forms.ModelForm):
    """Форма для добавления ингредиента"""
    
    class Meta:
        model = Ingredient
        fields = ['name', 'quantity', 'unit']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Название ингредиента'
            }),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Количество'
            }),
            'unit': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Единица измерения'
            }),
        }


class CookingStepForm(forms.ModelForm):
    """Форма для добавления шага приготовления"""
    
    class Meta:
        model = CookingStep
        fields = ['step_number', 'instruction']
        widgets = {
            'step_number': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Номер шага',
                'min': 1
            }),
            'instruction': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Опишите этот шаг...',
                'rows': 3
            }),
        }


# Formsets для динамического добавления ингредиентов и шагов
from django.forms import inlineformset_factory

IngredientFormSet = inlineformset_factory(
    Recipe,
    Ingredient,
    form=IngredientForm,
    extra=3,  # Количество пустых форм
    can_delete=True
)

CookingStepFormSet = inlineformset_factory(
    Recipe,
    CookingStep,
    form=CookingStepForm,
    extra=3,  # Количество пустых форм
    can_delete=True
)
