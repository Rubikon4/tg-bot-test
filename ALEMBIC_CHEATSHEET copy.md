# 📝 ALEMBIC ШПАРГАЛКА

## 🆕 Добавление новой таблицы

1. Создать модель SQLAlchemy (например, `Database/posts.py`)
2. Импортировать в `Database/migrations/env.py`
3. Создать миграцию:
   ```powershell
   cd Database
   alembic revision --autogenerate -m "Add posts table"
   ```
4. Проверить файл в `migrations/versions/`
5. Применить:
   ```powershell
   alembic upgrade head
   ```

---

## ➕ Добавление колонки в таблицу

1. Изменить модель (добавить новое поле)
2. Создать миграцию:
   ```powershell
   cd Database
   alembic revision --autogenerate -m "Add email to users"
   ```
3. Применить:
   ```powershell
   alembic upgrade head
   ```

---

## 🔧 Полезные команды

```powershell
# Текущая версия БД
alembic current

# История миграций
alembic history

# Откатить последнюю
alembic downgrade -1

# Откатить все
alembic downgrade base

# Показать SQL (без применения)
alembic upgrade head --sql
```

---

## ⚠️ ВАЖНЫЕ ПРАВИЛА

✅ **ВСЕГДА** используй `--autogenerate`  
✅ **ВСЕГДА** проверяй файл миграции перед применением  
✅ **Импортируй** все модели в `env.py`  
✅ **Запускай** команды из папки `Database`  
❌ **НЕ редактируй** примененные миграции

---

## 📂 Структура

```
Database/
  ├── alembic.ini          ← конфигурация
  ├── migrations/
  │   ├── env.py           ← импорты моделей
  │   ├── script.py.mako   ← шаблон
  │   └── versions/        ← файлы миграций
  ├── data.db              ← база данных
  └── users.py             ← модели
```
