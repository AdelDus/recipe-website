# ER-диаграмма базы данных для сайта рецептов

## Описание моделей

### 1. Category (Категория)
Модель для категоризации рецептов.

**Поля:**
- `id` (PK) - Первичный ключ
- `name` - Название категории (CharField, max_length=100, unique=True)
- `description` - Описание категории (TextField, blank=True)
- `icon` - Иконка категории (CharField, max_length=10)
- `created_at` - Дата создания (DateTimeField, auto_now_add=True)

**Связи:**
- One-to-Many с Recipe (одна категория может содержать много рецептов)

### 2. Recipe (Рецепт)
Основная модель, содержащая информацию о рецепте.

**Поля:**
- `id` (PK) - Первичный ключ
- `title` - Название рецепта (CharField, max_length=200)
- `description` - Описание блюда (TextField)
- `category_id` (FK) - Внешний ключ на Category (SET_NULL)
- `cooking_time` - Время приготовления в минутах (IntegerField)
- `servings` - Количество порций (IntegerField)
- `image` - Изображение блюда (ImageField)
- `likes` - Количество лайков (IntegerField, default=0)
- `created_at` - Дата создания (DateTimeField, auto_now_add=True)
- `updated_at` - Дата обновления (DateTimeField, auto_now=True)

### 3. Ingredient (Ингредиент)
Модель для хранения ингредиентов рецепта.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `name` - Название ингредиента (CharField, max_length=200)
- `quantity` - Количество (CharField, max_length=50)
- `unit` - Единица измерения (CharField, max_length=50)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много ингредиентов)

### 4. CookingStep (Шаг приготовления)
Модель для хранения пошаговых инструкций.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `step_number` - Номер шага (IntegerField)
- `instruction` - Текст инструкции (TextField)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много шагов)

### 6. Comment (Комментарий)
Модель для хранения комментариев пользователей.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `author_name` - Имя автора комментария (CharField, max_length=100)
- `text` - Текст комментария (TextField)
- `created_at` - Дата создания (DateTimeField, auto_now_add=True)

**Связи:**
- Many-to-One с Recipe (один рецепт может иметь много комментариев)

### 5. Favorite (Избранное)
Модель для хранения избранных рецептов пользователей.

**Поля:**
- `id` (PK) - Первичный ключ
- `recipe_id` (FK) - Внешний ключ на Recipe
- `session_key` - Ключ сессии пользователя (CharField, max_length=40)
- `created_at` - Дата добавления (DateTimeField, auto_now_add=True)

**Связи:**
- Many-to-One с Recipe (один рецепт может быть в избранном у многих пользователей)
- Уникальная пара (recipe, session_key) - один рецепт один раз в избранном у пользователя

## Визуальная диаграмма

```
┌──────────────────┐
│    Category      │
├──────────────────┤
│ id (PK)          │
│ name             │
│ description      │
│ icon             │
│ created_at       │
└──────────────────┘
         │
         │ 1
         │
         │ N
         ▼
┌─────────────────────────────────────┐
│           Recipe                    │
├─────────────────────────────────────┤
│ id (PK)                             │
│ title                               │
│ description                         │
│ category_id (FK)                    │
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

1. **Category → Recipe** (One-to-Many)
   - Одна категория может содержать множество рецептов
   - При удалении категории рецепты сохраняются (SET_NULL)

2. **Recipe → Ingredient** (One-to-Many)
   - Один рецепт может содержать множество ингредиентов
   - При удалении рецепта удаляются все связанные ингредиенты (CASCADE)

3. **Recipe → CookingStep** (One-to-Many)
   - Один рецепт может содержать множество шагов приготовления
   - При удалении рецепта удаляются все связанные шаги (CASCADE)

4. **Recipe → Comment** (One-to-Many)
   - Один рецепт может иметь множество комментариев
   - При удалении рецепта удаляются все связанные комментарии (CASCADE)

5. **Recipe → Favorite** (One-to-Many)
   - Один рецепт может быть в избранном у множества пользователей
   - При удалении рецепта удаляются все связанные записи избранного (CASCADE)
   - Уникальная пара (recipe, session_key)

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
