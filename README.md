# inno-python-practice
# Students & Rooms

Загрузка данных о студентах и комнатах из JSON-файлов в PostgreSQL, выполнение SQL-запросов
и выгрузка результата в JSON или XML.

## Возможности

- схема БД из двух таблиц со связью many-to-one (`students.room_id -> rooms.id`);
- пакетная загрузка данных без ORM, чистым SQL (psycopg2);
- четыре запроса, все вычисления выполняются на стороне БД;
- индексы под эти запросы (`sql/indexes.sql`);
- экспорт результата в JSON или XML;
- CLI с параметрами.

## Требования

- Python 3.10+
- Docker (для PostgreSQL) или любой доступный сервер PostgreSQL

## Установка

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

## База данных

Запустить PostgreSQL, например в Docker:

```bash
docker run --rm -v /var/run/docker.sock:/var/run/docker.sock assaflavie/runlike 04714e7b9a5c 
```

## Настройка

Подключение задаётся переменными окружения (значений по умолчанию нет).
Скопируйте шаблон и заполните его:

```bash
cp .env.example .env.local
set -a; source .env.local; set +a
```

| Переменная    | Описание          |
|---------------|-------------------|
| `DB_HOST`     | адрес сервера БД  |
| `DB_PORT`     | порт              |
| `DB_NAME`     | имя базы данных   |
| `DB_USER`     | пользователь      |
| `DB_PASSWORD` | пароль            |

## Запуск

Запускать из корня проекта:

```bash
python3 -m src.cli --rooms <путь/rooms.json> --students <путь/students.json> --format json
```

| Параметр     | Обязательный | Описание                                         |
|--------------|--------------|--------------------------------------------------|
| `--rooms`    | да           | путь к файлу с комнатами                         |
| `--students` | да           | путь к файлу со студентами                       |
| `--format`   | да           | формат результата: `json` или `xml`              |
| `--output`   | нет          | файл для результата (по умолчанию вывод в консоль) |

Пример с записью в файл:

```bash
python3 -m src.cli --rooms data/rooms.json --students data/students.json --format xml --output result.xml
```

Программу можно запускать повторно: схема и индексы создаются с `IF NOT EXISTS`,
данные загружаются через `INSERT ... ON CONFLICT DO UPDATE`. Вся загрузка выполняется
в одной транзакции.

## Формат входных данных

`rooms.json`: `[{"id": 0, "name": "Room #0"}, ...]`

`students.json`: `[{"id": 0, "name": "Peggy Ryan", "birthday": "2011-08-22T00:00:00.000000", "sex": "M", "room": 473}, ...]`

## Запросы

1. Список комнат и количество студентов в каждой.
2. Пять комнат с наименьшим средним возрастом студентов.
3. Пять комнат с наибольшей разницей в возрасте студентов.
4. Комнаты, в которых живут студенты разного пола.

Тексты запросов лежат в `sql/queries/`.

## Индексы

`sql/indexes.sql` создаёт три индекса: `students(room_id)`, `students(room_id, birthday)`,
`students(room_id, sex)`

## Структура проекта

```
sql/            схема, индексы, запросы
src/config.py   настройки из переменных окружения
src/models.py   модели Room и Student
src/loaders/    чтение входных файлов (DataLoader, JsonLoader)
src/db/         соединение с БД и репозитории
src/queries.py  QueryService (выполнение запросов)
src/exporters/  экспорт в JSON и XML
src/app.py      сценарий работы приложения
src/cli.py      командная строка
```