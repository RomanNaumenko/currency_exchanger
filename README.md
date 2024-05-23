# Currency Exchange API

Це API для обміну валют, який дозволяє відстежувати курси валют, зберігати історію курсів та керувати відслідковуванням валют. Проект реалізований на основі Django та Django REST Framework з використанням Celery для асинхронних задач і JWT для аутентифікації.

## Вимоги

- Python 3.9+
- Django 4.2+
- Django REST Framework
- Celery
- Redis
- PostgreSQL

## Встановлення

### Клонування репозиторію

```bash
git clone https://github.com/RomanNaumenko/currency_exchanger.git
cd currency_exchanger
```
### Віртуальне середовище
Створіть віртуальне середовище та активуйте його:
```
python3 -m venv .venv
source .venv/bin/activate  # Для Unix
.\venv\Scripts\activate  # Для Windows
```
### Встановлення залежностей
```
pip install -r requirements.txt
```

### Налаштування оточення

Створіть файл .env(використайте .env.sample) у кореневій папці проекту та додайте наступні змінні оточення:
```
DJANGO_SECRET_KEY=your_django_key
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=localhost, 127.0.0.1, 0.0.0.0

# Database settings
POSTGRES_DB=your_currency_db_name
POSTGRES_USER=your_user
POSTGRES_PASSWORD=your_password
POSTGRES_HOST=localhost
# db for docker
POSTGRES_PORT=5432

# Celery settings
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0

# Timezone
TIME_ZONE=Europe/Kiev
```
### Міграції бази даних
Застосуйте міграції для створення необхідних таблиць:

```
python manage.py makemigrations
python manage.py migrate
```

### Створення суперкористувача
Створіть суперкористувача для доступу до адміністративної панелі:
```
python manage.py createsuperuser your_super_user
```
### Запуск сервера
Запустіть локальний сервер:
```
python manage.py runserver
```

### Запуск Celery
Запустіть Celery для виконання асинхронних задач:

```
celery -A currency_exchanger worker -l info
celery -A currency_exchanger beat -l info
```

## Використання
### Аутентифікація
Для отримання доступу до захищених ендпоінтів API використовується JWT аутентифікація.
### Отримання токену:
```
POST /api/token/
{
    "username": "your_username",
    "password": "your_password"
}
```
### Оновлення токену:
```
POST /api/token/refresh/
{
    "refresh": "your_refresh_token"
}
```
### Ендпоінти
- GET /api/currency_rates/: Отримання списку валют з поточним курсом.
- GET /api/trackable_currencies/: Отримання списку валют, які можна додати для відслідковування.
- POST /api/add_trackable_currency/: Додавання нової валюти для відслідковування.
- GET /api/currency_rate_history/: Отримання історії курсу по конкретній валюті за конкретний період часу.
- PATCH /api/toggle_currency_tracking/{currency_code}/: Включення/відключення валюти з моніторингу.

### Документація API
Документацію API можна переглянути за допомогою Swagger UI за адресою:
```
http://localhost:8000/swagger/
```
### Менеджмент команди
- fetch_rates: Ця команда отримує курси валют з Monobank API та зберігає їх у базу даних.
```
python manage.py fetch_rates
```
- generate_csv: Ця команда створює локальний CSV файл зі списком валют і поточним курсом.
```
python manage.py generate_csv
```

### Docker
Для запуску проекту за допомогою Docker використовуйте наступні команду:
```
docker-compose up --build
```
