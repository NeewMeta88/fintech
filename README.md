
# 🏦 Bank API

RESTful API для управления банковскими счетами и переводами между ними. Подходит для использования в высоконагруженных финансовых системах.

## ⚙️ Стек технологий

- Python 3.10+
- Django 4.x + DRF
- PostgreSQL
- Kafka (Apache Kafka) — публикация событий
- Docker + docker-compose
- JWT авторизация

---

## 🚀 Быстрый старт

### 1. Клонируйте репозиторий

```bash
git clone https://github.com/your-user/bank-api.git
cd fintech
```

### 2. Создайте файл `.env` (необязательно для тестирования)
Пример содержимого:

```
SECRET_KEY=your-secret-key
DEBUG=True
POSTGRES_DB=bank_db
POSTGRES_USER=bank_user
POSTGRES_PASSWORD=bank_pass

KAFKA_KRAFT_MODE=true
KAFKA_CFG_PROCESS_ROLES=broker,controller
KAFKA_CFG_NODE_ID=1
KAFKA_CFG_CONTROLLER_LISTENER_NAMES=CONTROLLER
KAFKA_CFG_LISTENER_SECURITY_PROTOCOL_MAP=CONTROLLER:PLAINTEXT,PLAINTEXT:PLAINTEXT
KAFKA_CFG_LISTENERS=PLAINTEXT://:9092,CONTROLLER://:9093
KAFKA_CFG_ADVERTISED_LISTENERS=PLAINTEXT://kafka:9092
KAFKA_CFG_CONTROLLER_QUORUM_VOTERS=1@kafka:9093
ALLOW_PLAINTEXT_LISTENER=yes
```

## 🗃️ Начальные данные

Для тестирования можно провести миграции:

```bash
docker-compose exec web python manage.py migrate
```

Добавляется:
- суперпользователь `admin` (пароль: `admin`)
- пользователь `test` (пароль: `test`)
- 3 счёта пользователю `admin`
- 1 счет пользователю `test`

---

### 3. Запустите проект

```bash
docker-compose up --build
```

Проект будет доступен по адресу: [http://localhost:8000](http://localhost:8000)  
Имеется интерфейс для взаимодействия с api

---

## 🧪 Тесты

Запуск тестов:

```bash
docker-compose exec web python manage.py test app/
```

Проверяется:
- корректность бизнес-логики транзакций
- сохранение данных
- обработка ошибок

---

## 📚 API-эндпоинты

| Метод  | URL                                        | Описание                                           | Аутентификация |
| ------ | ------------------------------------------ | ---------------------------------------------------- |----------------|
| GET    | `/api/accounts/`                           | Получение счетов текущего пользователя               | ✅ Да           |
| POST   | `/api/accounts/`                           | Создание нового счёта                                | ✅ Да           |
| DELETE | `/api/accounts/{id}/`                      | Удаление счёта (если баланс = 0)                     | ✅ Да           |
| GET    | `/api/accounts/detail/{uuid}/`             | Открытие HTML-страницы с деталями счёта              | ✅ Да           |
| GET    | `/api/accounts/all`                        | Получение всех счетов (только для суперпользователя) | ✅ Да           |
| GET    | `/api/transactions/list/`                  | Получение списка транзакций текущего пользователя    | ✅ Да           |
| POST   | `/api/transactions/create/`                | Создание транзакции                                  | ✅ Да           |
| GET    | `/api/transactions/open-transaction-form/` | HTML-форма создания транзакции                       | ✅ Да           |
| POST   | `/api/token/`                              | Получение JWT-токена                                 | ❌ Нет          |
| GET    | `/register/`                               | Страница регистрации пользователя                    | ❌ Нет          |
| POST   | `/register/`                               | Регистрация нового пользователя                      | ❌ Нет          |
| GET    | `/`                                        | Страница входа (логин)                               | ❌ Нет          |
| POST   | `/`                                        | Вход пользователя                                    | ❌ Нет          |
| GET    | `/dashboard/`                              | Панель управления пользователя                       | ✅ Да           |
| GET    | `/logout/`                                 | Выход пользователя                                   | ✅ Да           |

---

## 💡 Бизнес-правила

- Нельзя переводить средства самому себе (на тот же счет)
- Сумма перевода должна быть положительной
- Недостаточный баланс — ошибка
- После перевода событие публикуется в Kafka (топик `transactions`)

---

## 💬 Kafka

Каждая транзакция отправляется в Kafka-топик `transactions`:

```json
{
  "id": "uuid",
  "from_account": "uuid",
  "to_account": "uuid",
  "amount": 500.00,
  "created_at": "2025-07-15T12:00:00Z"
}
```

Kafka запускается в составе `docker-compose`.

---

## 📜 История переводов (доп функционал)

Эндпоинт `/api/transactions/list/` возвращает список транзакций (только для суперпользователя), которые были совершены в отношении пользователя (получение/отправление средств).

Полезно для пользователей - они видят, что происходит со средствами на их счетах.

---

## 📎 Примеры curl

**🔐 Получить токен (JWT)**

```bash
curl -X POST http://localhost:8000/api/token/ \
-H "Content-Type: application/json" \
-d '{"username": "your_username", "password": "your_password"}'
```

**🏦 Создать счёт**

```bash
curl -X POST http://localhost:8000/api/accounts/ \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{}'
```
⚠️ `owner_name` не требуется — оно подставляется автоматически как username(index).

**💸 Создать перевод между счетами**

```bash
curl -X POST http://localhost:8000/api/transactions/create/ \
-H "Authorization: Bearer <token>" \
-H "Content-Type: application/json" \
-d '{
  "from_account": "<UUID_отправителя>",
  "to_account": "<UUID_получателя>",
  "amount": 100.0
}'
```

**🔁 Получить историю переводов**

```bash
curl -X GET http://localhost:8000/api/transactions/list/ \
-H "Authorization: Bearer <token>"
```

**📂 Получить список своих счетов**

```bash
curl -X GET http://localhost:8000/api/accounts/ \
-H "Authorization: Bearer <token>"
```

**🗑 Удалить счёт (если баланс = 0)**

```bash
curl -X DELETE http://localhost:8000/api/accounts/<UUID>/ \
-H "Authorization: Bearer <token>"
```

---

## 🧑‍💻 Автор

Родионов Егор Михайлович
