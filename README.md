📖 Проект Lalalai Anime Streaming Platform
Аниме-стриминг сервис с поддержкой коротких видео (Shorts), лайков, комментариев, системы избранного и рейтингов. Проект реализован на Django и ориентирован на удобное взаимодействие с пользователями.

📂 Содержание
Описание проекта

Основной функционал

Технологии

Установка и запуск проекта

Работа с базой данных

Тестирование

Контакты

📜 Описание проекта
Lalalai — это сайт для поиска и просмотра аниме-контента с возможностью:

Смотреть аниме и короткие видео (AMV, моменты).

Ставить лайки на шортах.

Оставлять комментарии к аниме, сезонам, эпизодам и шортам.

Добавлять аниме и шорты в избранное.

Оценивать аниме (система рейтингов).

🚀 Основной функционал
Регистрация и авторизация пользователей.

Разграничение ролей: Гость, Пользователь, Администратор.

Добавление аниме и сезонов через админ-панель.

Загрузка и публикация коротких видео (Shorts).

Лайки, избранное и комментарии.

Система оценок (звёздный рейтинг).

🛠 Технологии
Python 3.12

Django 5.x

SQLite / PostgreSQL (по выбору)

Tailwind CSS (для фронтенда)

Cloudinary (для хранения медиа)

JavaScript (управление лайками и короткими видео)

pytest / unittest (тестирование)

⚙️ Установка и запуск проекта
1. Клонирование репозитория
git clone https://github.com/your_username/lalalai-anime.git
cd lalalai-anime

2. Создание виртуального окружения
python -m venv venv
source venv/bin/activate   # для Linux/macOS
venv\Scripts\activate      # для Windows

3. Установка зависимостей
Редактировать
pip install -r requirements.txt

4. Настройка базы данных
По умолчанию используется SQLite.
Для настройки PostgreSQL нужно изменить параметры в settings.py:

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'your_db_name',
        'USER': 'your_db_user',
        'PASSWORD': 'your_db_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
5. Применение миграций
python manage.py makemigrations
python manage.py migrate
6. Создание суперпользователя
python manage.py createsuperuser
7. Запуск сервера
python manage.py runserver
Перейти в браузере по адресу:
http://127.0.0.1:8000/

🗄 Работа с базой данных
Примеры работы через Django ORM:

# Получить все аниме определённого жанра
Anime.objects.filter(genres__name='Фэнтези')

# Получить все комментарии к сезону
SeasonComment.objects.filter(season_id=1)

# Получить все шорты пользователя
Short.objects.filter(user=request.user)

🧪 Тестирование
Запуск тестов через Django Test Runner:
python manage.py test

Или через pytest (если установлен):
pytest

☁️ Интеграция Cloudinary
Проект использует Cloudinary для хранения медиафайлов (видео, изображения опенингов, постеры и т.д.), вместо локального хранения.

🔧 Шаги настройки Cloudinary
Зарегистрируйтесь на сайте cloudinary.com и создайте аккаунт.

Перейдите в Dashboard и найдите свои данные:
CLOUDINARY_CLOUD_NAME=your_cloud_name
CLOUDINARY_API_KEY=your_api_key
CLOUDINARY_API_SECRET=your_api_secret

Установите библиотеку Cloudinary для Python:
pip install cloudinary

В settings.py добавьте:
import cloudinary
import cloudinary.uploader
import cloudinary.api

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': os.getenv('CLOUDINARY_CLOUD_NAME'),
    'API_KEY': os.getenv('CLOUDINARY_API_KEY'),
    'API_SECRET': os.getenv('CLOUDINARY_API_SECRET'),
}

DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'
Добавьте эти переменные в .env или в системные переменные:
CLOUDINARY_CLOUD_NAME=lalalai123
CLOUDINARY_API_KEY=9876543210
CLOUDINARY_API_SECRET=supersecretkey

📥 Загрузка файлов
Django автоматически будет сохранять медиа в Cloudinary, если у моделей используется поле:
from cloudinary.models import CloudinaryField

class Opening(models.Model):
    title = models.CharField(max_length=100)
    video = CloudinaryField('video')


Загрузка будет происходить напрямую в облако — никаких MEDIA_ROOT не требуется!