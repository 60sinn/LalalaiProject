# LalalaiProject
## 🚀 Tailwind Setup for Windows (npm 10+)
npm init -y
npm install -D tailwindcss postcss autoprefixer tailwindcss-cli
npx tailwindcss init


📦 Cloudinary интеграция
Хранилище медиафайлов (аватары, постеры, видео) подключено через Cloudinary.

🔧 Что настроить в settings.py

CLOUDINARY_STORAGE = {
    'CLOUD_NAME': 'your_cloud_name',
    'API_KEY': 'your_api_key',
    'API_SECRET': 'your_api_secret',
}
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'


Для shell и ручных загрузок обязательно:

import cloudinary
cloudinary.config(
    cloud_name='your_cloud_name',
    api_key='your_api_key',
    api_secret='your_api_secret'
)


🛡️ Ограничения
Аватары ограничены по размеру и расширению:

Максимум: MAX_AVATAR_SIZE_KB = 4096 (в settings.py)

Разрешённые форматы: .jpg, .jpeg, .png, .webp

.gif временно запрещён

Валидаторы находятся в:
📁 users/validators.py