# 🐾 Barsik Utils
<details open>
<summary>🇺🇸 <b>English Version (click to expand)</b></summary>
Barsik is a comprehensive set of interfaces, base classes and utilities for accelerated development of applications and Telegram bots in Python. The library focuses on the principles of Clean Architecture, the use of Dependency Injection (Dishka) and a flexible adapter system.

## ✨ Key Features
  - 🔌 Adapter System: A sophisticated BaseAdapter class with automatic subclass registration, name generation from PascalCase, and easy discovery of available implementations.
  - 🤖 Telegram & aiogram-dialog:
    - Custom widgets for aiogram-dialog supporting multi-language localization.
    - Handlers for extracting Telegram User models into DTOs for DB processing.
    - Base UI layer (currently for aiogram-dialog, wxPython support planned).
  - 🌍 Geo Module (OSM): Advanced tools for OpenStreetMap integration: address lookup, distance calculation, and point-in-polygon/radius checks.
  - 🌐 Localization: Supports loading locales from .dat or .json. Can store data in-memory or in Redis.
  🗄 Working with the database (SQLAlchemy): * Universal BaseDBAdapter: Support for synchronous (Session) and asynchronous (AsyncSession) modes in one interface.
    - Universal BaseDBAdapter: Seamless support for both Synchronous (Session) and Asynchronous (AsyncSession) engines.
    - Session Lifecycle Management: Built-in async context manager support (async with) to handle session opening, closing, and engine disposal.
    - flexible configuration: Creating an Engine based on a configuration object and linking models through a declarative base.
    - Adapters for SQLite (PostgreSQL support in progress).
    - Base user classes, entity mixins (ID, Timefields), and data interactors.
  - Common interface for storage backends (Redis / Memory).
  - 🛠 HTTP Utilities: Base sync and async clients powered by Descanso. Includes a built-in Google Translate module.
  - 💉 Dependency Injection: All services and tools are designed to work seamlessly with Dishka providers.
</details>

<details>
<summary>🇺🇦 <b>Українська версія (натисніть, щоб розгорнути)</b></summary>
Barsik — це комплексний набір інтерфейсів, базових класів та утиліт для прискореної розробки додатків та Telegram-ботів на Python. Бібліотека фокусується на принципах Clean Architecture, використанні Dependency Injection (Dishka) та гнучкій системі адаптерів.

## ✨ Основні можливості
  - 🔌 Система Адаптерів: Базовий клас BaseAdapter з автоматичною реєстрацією підкласів, генерацією імен на основі PascalCase та зручним доступом до доступних реалізацій.
  - 🤖 Telegram & aiogram-dialog:
    -Спеціальний віджет для aiogram-dialog із вбудованою локалізацією текстів.
    - Хендлери для автоматичного отримання DTO моделі User із Telegram.
    - Базовий UI-інтерфейс (у планах підтримка wxPython для десктопу).
  - 🌍 Гео-модуль (OSM): Потужні інструменти для роботи з OpenStreetMap: пошук адрес, вимірювання дистанцій, перевірка знаходження точки в радіусі або полігоні.
  - 🌐 Локалізація: Підтримка завантаження перекладів з .dat та .json файлів. Робота як з пам'яттю (In-Memory), так і з Redis.
  🗄 Робота з БД (SQLAlchemy): * Універсальний BaseDBAdapter: Підтримка синхронного (Session) та асинхронного (AsyncSession) режимів в одному інтерфейсі.
    - Автоматичне керування сесіями: Реалізація асинхронного контекстного менеджера (async with) для автоматичного відкриття та закриття сесій.
    - Гнучка конфігурація: Створення Engine на основі об'єкта конфігурації та прив'язка моделей через declarative_base.
    - Адаптери для SQLite (у розробці PostgreSQL).
    - Базові класи користувачів, міксини (ID, Timestamps) та інтерактори.
  - Уніфікований інтерфейс сховищ (Redis / Memory).
  - 🛠 HTTP Клієнти: Синхронні та асинхронні клієнти на базі Descanso. Включає вбудований модуль перекладу (Google Translate).
  - 💉 Dependency Injection: Повна інтеграція з Dishka для прозорого керування сервісами.
</details>
<details>
<summary>- <b>Русская версия (нажмите, чтобы развернуть)</b></summary>
Barsik — это комплексный набор интерфейсов, базовых классов и утилит для ускоренной разработки приложений и Telegram-ботов на Python. Библиотека фокусируется на принципах Clean Architecture, использовании Dependency Injection (Dishka) и гибкой системе адаптеров.

## ✨ Основные возможности
  - 🔌 Система Адаптеров: Базовый класс BaseAdapter с автоматической регистрацией подклассов, генерацией имен на основе PascalCase и удобным доступом к доступным реализациям.
  - 🤖 Telegram & aiogram-dialog:
    -Специальный виджет для aiogram-dialog со встроенной локализацией текстов.
    - Хендлеры для автоматического получения DTO модели User из Telegram.
    - базовый UI-интерфейс (в планах поддержка wxPython для рабочего стола).
  - 🌍 Гео-модуль (OSM): Мощные инструменты для работы с OpenStreetMap: поиск адресов, измерение дистанций, проверка нахождения точки в радиусе или полигоне.
  - 🌐 Локализация: Поддержка загрузки переводов из .dat и .json файлов. Работа как с памятью (In-Memory), так и с Redis.
  🗄 Работа с БД (SQLAlchemy): * Универсальный BaseDBAdapter: Поддержка синхронного (Session) и асинхронного (AsyncSession) режимов в одном интерфейсе.
    - Автоматическое управление сессиями: Реализация асинхронного контекстного менеджера (async with) для автоматического открытия и закрытия сессий.
    - гибкая конфигурация: Создание Engine на основе объекта конфигурации и привязка моделей через declarative base.
    - адаптеры для SQLite (в разработке PostgreSQL).
    - базовые классы пользователей, миксины (ID, Timestamps) и интеракторы.
  - унифицированный интерфейс хранилищ (Redis/Memory).
  - 🛠 HTTP Клиенты: Синхронные и асинхронные клиенты на основе Descanso. Включает встроенный модуль перевода (Google Translate).
  - 💉 Dependency Injection: Полная интеграция с Dishka для прозрачного управления сервисами.
</details>

## Author: Ruslan Dolovaniuk
