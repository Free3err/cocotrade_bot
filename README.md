# CoconutBot (CocoTrade)

## Авторы проекта
* Ryan Gosling

## Описание идеи
CoconutBot - это торговый бот для Telegram, созданный для управления виртуальной экономической системой. Он предоставляет пользователям возможность управлять фермой, проводить исследования технологий, совершать покупки в магазине и администрировать аккаунты.

## Описание реализации
Проект разделен на две основные части: бот (Telegram интерфейс) и серверное API (Flask). Бот реализован с использованием библиотеки aiogram и следует модульной архитектуре с выделенными обработчиками для различных функциональных блоков (ферма, технологии, магазин, администрирование). Серверная часть построена на Flask и Flask-RESTX для создания RESTful API, к которому обращается бот. Для организации запланированных задач используется APScheduler. Проект полностью контейнеризирован с помощью Docker для упрощения деплоя.

Ключевые классы и компоненты:
* `CocoTradeBot` - основной класс бота, инициализирующий диспетчер и обработчики
* Модульные обработчики: MainMenu, Farm, Technology, Store, Admin
* Flask API с документацией на Swagger (доступно по пути `/docs`)
* Использование SQLAlchemy для работы с базой данных

## Используемые технологии
* **Язык программирования:** Python 3.11
* **Фреймворки и библиотеки:**
  * aiogram 3.20+ (Telegram Bot API)
  * Flask 3.1.0 (Web API)
  * Flask-RESTX (API документация)
  * SQLAlchemy (ORM)
  * APScheduler (планировщик задач)
  * YooKassa (платежная система)
  * python-dotenv (управление переменными окружения)

## Инструкция по запуску
1. Клонировать репозиторий
2. Создать файл `.env` с переменными окружения:
   ```
   TOKEN=your_telegram_bot_token
   SECRET_KEY=your_secret_key
   ```
3. Запустить с помощью Docker Compose:
   ```
   docker-compose up -d
   ```

Альтернативный запуск (без Docker):
1. Установить зависимости: `pip install -r requirements.txt`
2. Запустить сервер: `python -m server.run`
3. Запустить бота: `python -m bot.main`

## Структура проекта
```
CoconutBot/
├── bot/                  # Код Telegram бота
│   ├── handlers/         # Обработчики команд бота
│   ├── services/         # Сервисные функции
│   ├── config.py         # Конфигурация бота
│   └── main.py           # Точка входа бота
├── server/               # Серверная часть
│   ├── app/              # Приложение Flask
│   │   ├── api/          # API эндпоинты
│   │   ├── instance/     # Файлы базы данных
│   │   ├── services/     # Бизнес-логика
│   │   └── utils/        # Вспомогательные функции
│   └── run.py            # Точка входа сервера
├── requirements.txt      # Зависимости проекта
├── Dockerfile            # Инструкции для сборки образа
└── docker-compose.yml    # Конфигурация Docker Compose
``` 