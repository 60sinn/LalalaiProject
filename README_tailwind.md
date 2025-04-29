# 🌸 Tailwind CSS Setup (LalalaiProject)

Этот проект использует **актуальную установку Tailwind CSS** через `@tailwindcss/cli`, как указано в официальной документации:  
🔗 https://tailwindcss.com/docs/installation/tailwind-cli

---

## 📦 Установка

```bash
npm install -D tailwindcss @tailwindcss/cli
```

---

## 📄 Входной CSS (`static/src/input.css`)

```css
@import "tailwindcss";
```

> Файл уже создан. Содержит только одну строку — `@import "tailwindcss";`

---

## 🚀 Запуск сборки Tailwind

```bash
npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --watch
```

Или через скрипт в `package.json`:

```json
"scripts": {
  "dev": "npx @tailwindcss/cli -i ./static/src/input.css -o ./static/css/output.css --watch"
}
```

Для запуска:
```bash
npm run dev
```

---

## 🧠 Примечания

- Tailwind собирает стили **только для реально используемых классов**
- Шаблоны сканируются по путям в `tailwind.config.js`
- Подключение `output.css` уже прописано в `base.html`:

```html
<link href="{% static 'css/output.css' %}" rel="stylesheet">
```

---

> Установка протестирована и стабильна. Используй `npm run dev` в процессе разработки.