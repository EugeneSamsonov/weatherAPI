
# WeatherAPI

WeatherAPI — это приложение, разработанное на Python с использованием Django и Django REST Framework. Оно предоставляет API для получения и обработки данных о погоде.

## Функциональность

- **Пользователи**: регистрация, аутентификация и управление пользователями.
- **Погода**: получение текущей погоды, исторических данных и прогнозов.
- **Docker**: возможность контейнеризации приложения для удобного развертывания.

## API endpoints

<p><code>api/v1/weather/&lt;slug:city&gt;</code> — получение погоды для конкретного города</p>
<p><code>api/v1/weather/</code> — получение общей информации о погоде (базовый URL)</p>
<p><code>api/register/</code> — регистрация пользователя</p>
<p><code>api/token/</code> — получение токена авторизации</p>
<p><code>api/token/refresh/</code> — обновление токена авторизации</p>
<p><code>api/v1/history/</code> — получение истории запросов пользователя (базовый URL)</p>
<p><code>api/v1/history/{id}</code> — получение истории запросов пользователя по идентификатору</p>


## Технологии

- Python
- Django (DRF)
- Docker
- JWT авторизация
- Redis
- PostgreSQL
- Django tests

## Установка и запуск (без Docker)
**Убедитесь, что у вас установлены, включёны и прослушиватся порты Redis (6379) и Postgres (5432)**.
1. **Клонирование репозитория**:

   ```bash
   git clone https://github.com/EugeneSamsonov/weatherAPI.git
   ```

2. **Расспакуйте архив (пароль weatherapi)**:
3. **Перейдите в директорию проекта**:

   ```bash
   cd weatherAPI
   ```

4. **Создайте и активируйте виртуальное окружение**:

   ```bash
   python3 -m venv env

   (linux)
   source env/bin/activate

   (win)
   .venv\Scripts\activate
   ```

5. **Установите зависимости**:

   ```bash
   pip install -r requirements.txt
   ```

6. **Выполните миграции базы данных**:

   ```bash
   python manage.py migrate
   ```

7. **Запустите сервер разработки**:

   ```bash
   python manage.py runserver
   ```

   Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

## Использование Docker

Для запуска приложения в контейнере Docker:

1. **Убедитесь, что у вас установлен Docker**.
2. **Расспакуйте архив (пароль указан выше)**
3. **Соберите и запустите контейнеры**:

   ```bash
   docker-compose up --build
   ```

   Приложение будет доступно по адресу `http://127.0.0.1:8000/`.

## Тестирование

Для запуска тестов используйте команду:
(Не забывайте включить redis и postgres)

```bash
python manage.py test
```

## Контакты

По вопросам и предложениям обращайтесь к автору проекта: [EugeneSamsonov](https://github.com/EugeneSamsonov).
