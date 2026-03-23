# JSON FileReader

Веб-приложение на Django для загрузки JSON файлов в базу данных MySQL с отображением записей через DataTables.

## Возможности

- Загрузка JSON файла через форму
- Валидация каждой записи (формат, длина, наличие полей)
- Сохранение валидных данных в MySQL
- Просмотр всех записей в таблице с поиском и сортировкой (DataTables)

## Требования 

- Python 3.10+
- MySQL 8.0+

## Установка и запуск

### 1. Клонировать репозиторий

```bash
git clone <ссылка на репозиторий>
cd filereader
```

### 2. Создать и активировать виртуальное окружение

```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Установить зависимости

```bash
pip install django mysqlclient django-environ
```

### 4. Создать базу данных MySQL

```bash
sudo mysql
```

```sql
CREATE DATABASE filereader CHARACTER SET utf8mb4;
CREATE USER 'django_user'@'localhost' IDENTIFIED BY 'MyPass123!';
GRANT ALL PRIVILEGES ON filereader.* TO 'django_user'@'localhost';
FLUSH PRIVILEGES;
EXIT;
```

### 5. Настроить переменные окружения

Создать файл `env` в папке `filereader/`:

```
SECRET_KEY=твой_секретный_ключ
```

### 6. Настроить базу данных в settings.py

В файле `filereader/settings.py` указать данные подключения к MySQL:

```python
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.mysql",
        "NAME": "filereader",
        "USER": "django_user",
        "PASSWORD": "MyPass123!",
        "HOST": "localhost",
        "PORT": "3306",
    }
}
```

### 7. Применить миграции

```bash
python3 manage.py migrate
```

### 8. Запустить сервер

```bash
python3 manage.py runserver
```

Открыть в браузере: [http://127.0.0.1:8000](http://127.0.0.1:8000)

## Формат JSON файла

```json
[
    {
        "name": "John Doe",
        "date": "2024-01-15_10:30"
    },
    {
        "name": "Jane Smith",
        "date": "2024-03-22_14:00"
    }
]
```

### Правила валидации

- `name` — обязательное поле, строка длиной **менее 50 символов**
- `date` — обязательное поле, формат **YYYY-MM-DD_HH:mm**
- Лишние ключи игнорируются
- При любой ошибке — ничего не сохраняется, пользователь видит список ошибок

## Страницы

| URL | Описание |
|-----|----------|
| `/` | Форма загрузки JSON файла |
| `/datatable/` | Таблица со всеми записями |
