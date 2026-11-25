# Структура даних

**Проєкт:** Система управління послугами хімчистки (варіант 12)
**Рівень складності:** I (високий, 10–12 балів)
**Діаграми:** [class-diagram.png](class-diagram.png), [er-diagram.png](er-diagram.png)
**Вимоги:** [requirements.md](requirements.md)

## 1. Класи предметної області

Програма має чотири основні класи та два переліки (enum). Переліки не є сутностями, але використовуються як типи атрибутів.

| Клас | Призначення | Основні атрибути | Основні методи |
|---|---|---|---|
| `Client` | Клієнт хімчистки | id: int, fullName: str, phone: str, registeredAt: date, orders: list[Order] | update(), hasActiveOrders(), isRegular() |
| `Service` | Позиція прайс-листа | id: int, name: str, basePrice: Decimal, durationDays: int, isActive: bool | update(), activate(), deactivate(), isAvailable() |
| `Order` | Замовлення (квитанція) | number: int, client: Client, acceptedAt, readyDate, isUrgent, status: OrderStatus, discount, totalPrice, issuedAt, items: list[OrderItem] | addItem(), removeItem(), calculateTotal(), calculateReadyDate(), changeStatus(), cancel(), issue() |
| `OrderItem` | Річ у замовленні | id: int, itemType: str, material: Material, color: str, defects: str, price: Decimal, services: dict[Service, Decimal] | addService(), removeService(), calculatePrice(), hasService() |
| `OrderStatus` (enum) | Стан замовлення | ACCEPTED, IN_PROGRESS, READY, ISSUED, CANCELLED | — |
| `Material` (enum) | Матеріал речі та його коефіцієнт | NORMAL (1.0), DELICATE (1.3), LEATHER_FUR (1.5) | coefficient() |

### Пояснення атрибутів

- **`services: dict[Service, Decimal]`** — словник «послуга → ціна на момент оформлення». Зберігає ціну, яка діяла під час прийняття речі, тож зміна прайс-листа не впливає на вже оформлені замовлення (BR-11).
- **`Order.number`** — це номер квитанції, який видає система. Він же є первинним ключем у таблиці `orders`.
- **`Order.discount`** — знижка постійного клієнта (5 %, BR-05), розрахована й зафіксована на момент оформлення.

## 2. Зв'язки між класами

| Зв'язок | Тип | Кратність | Пояснення |
|---|---|---|---|
| Client — Order | Асоціація | 1 — 0..* | Клієнт може мати довільну кількість замовлень. Замовлення належить одному клієнту. |
| Order — OrderItem | Композиція | 1 — 1..20 | Річ існує лише як частина замовлення. Без замовлення її немає. Обмеження 1..20 з BR-07. |
| OrderItem — Service | Асоціація (багато-до-багатьох) | 0..* — 1..* | Річ має щонайменше одну послугу, а послуга може використовуватися в багатьох речах. Реалізується через проміжну таблицю `order_item_services`. |
| Order — OrderStatus | Залежність | — | Атрибут `status` має тип переліку. |
| OrderItem — Material | Залежність | — | Атрибут `material` має тип переліку. Коефіцієнт використовується в BR-03. |

## 3. Де і як зберігаються об'єкти

- **Місце зберігання:** SQLite, файл `chemclean.db` у папці проєкту. Файл створює модуль `database.py` під час першого запуску (FR-29).
- **Робота з об'єктами:** під час роботи програми об'єкти класів створюються з рядків таблиць і після змін записуються назад. Модуль `database.py` містить функції для читання й запису кожної таблиці, а `services.py` містить бізнес-логіку.
- **Списки в пам'яті:** атрибути `Client.orders`, `Order.items` та `OrderItem.services` заповнюються з бази даних під час завантаження об'єкта. Вони не є окремим сховищем.
- **Параметризовані запити:** усі значення від користувача передаються в SQL через параметри `?`, а не через рядкове об'єднання (вимога розділу 10 інструкції).
- **Транзакції:** кожна операція, яка змінює кілька таблиць (наприклад, оформлення замовлення разом з речами та послугами), виконується в одній транзакції. У разі помилки виконується rollback (E-19).
- **Ідентифікатори:** первинні ключі `INTEGER PRIMARY KEY AUTOINCREMENT` видаються базою даних, окрім `order_item_services`, де ключем є пара (item_id, service_id).

## 4. Таблиці бази даних

Усі таблиці нижче відповідають ER-діаграмі.

### 4.1. `clients`

| Поле | Тип | Обмеження | Опис |
|---|---|---|---|
| `client_id` | INTEGER | **PRIMARY KEY**, AUTOINCREMENT | Ідентифікатор клієнта |
| `full_name` | TEXT | NOT NULL | ПІБ (BR-01) |
| `phone` | TEXT | NOT NULL, **UNIQUE** | Телефон у форматі `+380XXXXXXXXX` (BR-01) |
| `registered_at` | TEXT | NOT NULL | Дата реєстрації у форматі ISO `YYYY-MM-DD` |

### 4.2. `services`

| Поле | Тип | Обмеження | Опис |
|---|---|---|---|
| `service_id` | INTEGER | **PRIMARY KEY**, AUTOINCREMENT | Ідентифікатор послуги |
| `name` | TEXT | NOT NULL, UNIQUE | Назва (BR-02) |
| `base_price` | NUMERIC | NOT NULL, CHECK (base_price > 0 AND base_price <= 100000) | Базова ціна, грн |
| `duration_days` | INTEGER | NOT NULL, CHECK (duration_days BETWEEN 1 AND 30) | Тривалість виконання |
| `is_active` | INTEGER | NOT NULL, DEFAULT 1 | 1 — активна, 0 — деактивована (BR-11) |

### 4.3. `orders`

| Поле | Тип | Обмеження | Опис |
|---|---|---|---|
| `order_id` | INTEGER | **PRIMARY KEY**, AUTOINCREMENT | Номер замовлення (квитанції) |
| `client_id` | INTEGER | NOT NULL, **FOREIGN KEY** → `clients.client_id` | Клієнт замовлення |
| `accepted_at` | TEXT | NOT NULL | Дата приймання |
| `ready_date` | TEXT | NOT NULL | Планована дата готовності (BR-06) |
| `is_urgent` | INTEGER | NOT NULL, DEFAULT 0 | Ознака терміновості |
| `discount` | NUMERIC | NOT NULL, DEFAULT 0 | Знижка постійного клієнта (BR-05) |
| `total_price` | NUMERIC | NOT NULL | Загальна вартість |
| `status` | TEXT | NOT NULL, CHECK (status IN ('ACCEPTED','IN_PROGRESS','READY','ISSUED','CANCELLED')) | Статус (BR-08) |
| `issued_at` | TEXT | NULL | Дата видачі, заповнюється лише для статусу ISSUED (BR-13) |

### 4.4. `order_items`

| Поле | Тип | Обмеження | Опис |
|---|---|---|---|
| `item_id` | INTEGER | **PRIMARY KEY**, AUTOINCREMENT | Ідентифікатор речі |
| `order_id` | INTEGER | NOT NULL, **FOREIGN KEY** → `orders.order_id` | Замовлення, до якого належить річ |
| `item_type` | TEXT | NOT NULL | Тип виробу |
| `material` | TEXT | NOT NULL, CHECK (material IN ('NORMAL','DELICATE','LEATHER_FUR')) | Матеріал (BR-03) |
| `color` | TEXT | NOT NULL | Колір |
| `defects` | TEXT | NULL | Опис дефектів (необов'язково) |
| `price` | NUMERIC | NOT NULL | Вартість речі після коефіцієнта матеріалу |

### 4.5. `order_item_services` (проміжна таблиця)

| Поле | Тип | Обмеження | Опис |
|---|---|---|---|
| `item_id` | INTEGER | **PRIMARY KEY (разом із service_id)**, **FOREIGN KEY** → `order_items.item_id` | Річ |
| `service_id` | INTEGER | **PRIMARY KEY (разом із item_id)**, **FOREIGN KEY** → `services.service_id` | Послуга |
| `price_snapshot` | NUMERIC | NOT NULL | Ціна послуги на момент оформлення (BR-11) |

Складений первинний ключ `(item_id, service_id)` не дає вибрати ту саму послугу двічі для однієї речі (E-09) навіть у разі помилки в коді.

## 5. Первинні та зовнішні ключі

| Таблиця | Первинний ключ | Зовнішній ключ | Посилається на | Поведінка при видаленні |
|---|---|---|---|---|
| `clients` | `client_id` | — | — | — |
| `services` | `service_id` | — | — | Видалення заборонене, якщо є записи в `order_item_services` (BR-11) |
| `orders` | `order_id` | `client_id` | `clients.client_id` | Видалення клієнта заборонене, якщо є активні замовлення (BR-10) |
| `order_items` | `item_id` | `order_id` | `orders.order_id` | `ON DELETE CASCADE` |
| `order_item_services` | (`item_id`, `service_id`) | `item_id`, `service_id` | `order_items.item_id`, `services.service_id` | `ON DELETE CASCADE` для `item_id` |

У SQLite зовнішні ключі вмикаються командою `PRAGMA foreign_keys = ON;`, яку виконує `database.py` при кожному з'єднанні.

## 6. Відповідність бізнес-правилам

| Правило | Як реалізовано в структурі даних |
|---|---|
| BR-01 | UNIQUE на `clients.phone`; формат перевіряється в коді |
| BR-02 | UNIQUE на `services.name`; CHECK на `base_price` і `duration_days` |
| BR-08 | CHECK на `orders.status`; допустимі переходи перевіряються в `services.py` |
| BR-10 | Видалення клієнта перевіряється в коді за статусами замовлень |
| BR-11 | Ціна фіксується в `price_snapshot`; `is_active` замість видалення послуги |

## 7. Обґрунтування вибору SQLite

- Модуль `sqlite3` входить до стандартної бібліотеки Python, тож не потрібні сторонні залежності.
- Структура даних реляційна: є зв'язки 1:N і N:M, які зручно описувати через ключі й обмеження.
- Потрібні транзакції та обмеження цілісності, які SQLite підтримує.
