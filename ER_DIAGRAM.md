# ER-диаграмма базы данных для сайта рецептов

## Описание моделей

### 1. Recipe (Рецепт)
Основная модель, содержащая информацию о рецепте.

**Поля:**
- `id` (PK) - Первичный ключ
- `title` - Название рецепта (CharField, max_length=200)
- `description` - Описание блюда (TextField)
- `cooking_time` - Время приготовления в минутах (IntegerField)
- `servings` - Количество порций (IntegerField)
- `image` - Изображение блюда (ImageField)
- `created_at` - Дата создания (DateTimeField, auto_now_add=True)
- `updated_at` - Дата обновления (DateTimeField, auto_now=True)

### 2. Ingredient (Ингредиент)
Модель для хранения ингредиентов рецепта.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `name` - Название ингредиента (CharField, max_length=200)
- `quantity` - Количество (CharField, max_length=50)
- `unit` - Единица измерения (CharField, max_length=50)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много ингредиентов)

### 3. CookingStep (Шаг приготовления)
Модель для хранения пошаговых инструкций.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `step_number` - Номер шага (IntegerField)
- `instruction` - Текст инструкции (TextField)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много шагов)

### 4. Comment (Комментарий)
Модель для хранения комментариев пользователей.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `author_name` - Имя автора комментария (CharField, max_length=100)
- `text` - Текст комментария (TextField)
- `created_at` - Дата создания (DateTimeField, auto_now_add=True)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много комментариев)

## Визуальная диаграмма

```
┌─────────────────────────────────────┐
│           Recipe                    │
├─────────────────────────────────────┤
│ id (PK)                             │
│ title                               │
│ description                         │
│ cooking_time                        │
│ servings                            │
│ image                               │
│ likes                               │
│ created_at                          │
│ updated_at                          │
└─────────────────────────────────────┘
         │              │            │
         │ 1            │ 1          │ 1
         │              │            │
         │ N            │ N          │ N
         ▼              ▼            ▼
┌──────────────┐ ┌──────────────┐ ┌──────────────┐
│ Ingredient   │ │ CookingStep  │ │  Comment     │
├──────────────┤ ├──────────────┤ ├──────────────┤
│ id (PK)      │ │ id (PK)      │ │ id (PK)      │
│ recipe_id(FK)│ │ recipe_id(FK)│ │ recipe_id(FK)│
│ name         │ │ step_number  │ │ author_name  │
│ quantity     │ │ instruction  │ │ text         │
│ unit         │ │              │ │ created_at   │
└──────────────┘ └──────────────┘ └──────────────┘
```

## Связи между таблицами

1. **Recipe → Ingredient** (One-to-Many)
   - Один рецепт может содержать множество ингредиентов
   - При удалении рецепта удаляются все связанные ингредиенты (CASCADE)

2. **Recipe → CookingStep** (One-to-Many)
   - Один рецепт может содержать множество шагов приготовления
   - При удалении рецепта удаляются все связанные шаги (CASCADE)

## Индексы и оптимизация

- Индекс на `recipe_id` в таблицах Ingredient и CookingStep для быстрого поиска
- Индекс на `created_at` в Recipe для сортировки по дате
- Индекс на `step_number` в CookingStep для правильной сортировки шагов

## Примеры запросов

```python
# Получить рецепт со всеми ингредиентами и шагами
recipe = Recipe.objects.get(id=1)
ingredients = recipe.ingredients.all()
steps = recipe.steps.all()

# Получить все рецепты с временем приготовления менее 30 минут
quick_recipes = Recipe.objects.filter(cooking_time__lt=30)

# Получить рецепты, отсортированные по дате создания
recent_recipes = Recipe.objects.order_by('-created_at')
```
