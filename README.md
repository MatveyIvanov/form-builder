# Form Builder
![Static Badge](https://img.shields.io/badge/python-3.11-brightgreen?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/FastAPI-0.112.0-brightgreen?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/flake8-passing-brightgreen?style=flat&logo=python)
![Static Badge](https://img.shields.io/badge/mypy-passing-brightgreen?style=flat&logo=python)

## Оглавление
* [Разворачивание проекта](#разворачивание-проекта)
    * [Зависимости](#зависимости)
    * [Окружение](#окружение)
    * [Запуск в локальном окружении](#запуск-в-локальном-окружении)
    * [Запуск в тестовом окружении](#запуск-в-тестовом-окружении)
   * [После запуска](#после-запуска)
* [Проверка работы](#проверка-работы)
* [Запуск flake8](#запуск-flake8)
* [Запуск mypy](#запуск-mypy)
* [Разработка](#разработка)
    * [Форматирование кода](#форматирование-кода)
    * [Git хуки](#git-хуки)

## Разворачивание проекта
### Зависимости
* docker
* docker compose v2
* python 3.8+ (опционально, для локального запуска flake8/mypy)
* poetry (опционально, для локального запуска flake8/mypy)
### Окружение
Перед запуском контейнеров, необходимо убедиться, что директории [docker](./docker/) присутствует файл `.env`, в котором заполнены все необходимые переменные окружения.<br>
Названия этих переменных можно посмотреть в [.env.example](./docker/.env.example)<br>

<details>
<summary><b>Подробное описание переменных окружения</b></summary>
<p>

#### PROJECT_NAME
Название проекта
#### DEBUG
Режим отладки<br>
0 - выключен<br>
1 - включен<br>
Если включен, то:
* 500 ошибки сервера не будут обработаны обработчиком исключений
#### Database
Доступы к БД
#### Nginx
NGINX_OUTER_PORT - порт, через который можно обращаться к контейнеру nginx<br>
NGINX_INNER_PORT - порт, на который будут переадресовываться все запросы внутри контейнера nginx<br>
#### ASGI
ASGI_PORT - порт, по которому можно обращаться к asgi сервису
#### Logging
LOGGING_SENSITIVE_FIELDS - чувствительные поля, которые нужно игнорировать при записи лога. Должны быть разделены через запятую, без пробелов<br>
LOGGING_LOGGERS - названия логеров. Должны быть разделены через запятую, без пробелов<br>
LOGGING_MAX_BYTES - максимальное кол-во байт на один лог файл<br>
LOGGING_BACKUP_COUNT - максимальное кол-во бэкап файлов для логов<br>
#### Docker Compose Specific
RESTART_POLICY - политика рестарта контейнеров<br>
NGINX_VERSION - версия Nginx<br>
MONGO_VERSION - версия MongoDB<br>
ASGI_TARGET - образ для сборки asgi сервиса<br>
*_CPUS - лимит ядер на контейнер<br>
*_MEM_LIMIT - лимит памяти на контейнер<br>
*_MEM_RESERVATION - запас памяти на контейнер<br>

</p>
</details>

Пример локального окружения для проверки работы:
```ini
# FastAPI project
PROJECT_NAME=formbuilder
DEBUG=1

# Database
DB_NAME=formbuilder
DB_USER=formbuilder
DB_PASSWORD=password
DB_HOST=db
DB_PORT=27017

# Nginx
NGINX_OUTER_PORT=8000
NGINX_INNER_PORT=5000

# ASGI
ASGI_PORT=8000

# Logging
LOGGING_MAX_BYTES=1024
LOGGING_BACKUP_COUNT=0

# Docker Compose Specific
RESTART_POLICY=unless-stopped
NGINX_VERSION=1.27.1-alpine
MONGO_VERSION=8.0.3
ASGI_TARGET=dev-asgi

```

### Запуск в локальном окружении
```bash
make localup
```
### Запуск в тестовом окружении
```bash
make developup
```
### После запуска
Проект станет доступен по порту \${NGINX_OUTER_PORT}<br>
В локальном окружении достаточно перейти по адресу http://localhost:\${NGINX_OUTER_PORT}/<br>
В другом окружении необходимо настроить домен, при обращении к которому веб-сервер (Nginx/Apache) будет проксировать все запросы на порт \${NGINX_OUTER_PORT}

## Проверка работы
В директории [src](./src) есть файл [forms.json](./src/forms.json), в котором описаны формы, загружаемые в БД при запуске сервиса.
Актуальную схему документа формы в коллекции `forms` можно найти в файле [form.py](./src/schemas/form.py) (класс `FormMongo`).

Запросы для тестирования формы `User Form`:
* Полное совпадение по переданным параметрам (формат даты `YYYY-mm-dd`) - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?first_name=Test&last_name=Testov&email=email%40email.com&phone=%2B79062419744&birth_date=2024-01-01'
    ```

* Полное совпадение по переданным параметрам (формат даты `dd.mm.YYYY`) - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?first_name=Test&last_name=Testov&email=email%40email.com&phone=%2B79062419744&birth_date=01.01.2024'
    ```

* Полное совпадение с лишним полем `unknown` - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?first_name=Test&last_name=Testov&email=email%40email.com&phone=%2B79062419744&birth_date=01.01.2024&unknown=value'
    ```

* Полное совпадение по названию полей, но дата рождения не совпадает по типу - ожидается список полей с их типами

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?first_name=Test&last_name=Testov&email=email%40email.com&phone=%2B79062419744&birth_date=date'
    ```

* Полное совпадение по типам, но не хватает поля `email` - ожидается список полей с их типами

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?first_name=Test&last_name=Testov&phone=%2B79062419744&birth_date=01.01.2024'
    ```

Запросы для тестирования формы `Order Form`:
* Полное совпадение по переданным параметрам (формат даты `YYYY-mm-dd`) - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?address=Test&ship_date=2024-01-01&agent_phone=%2B79062419744&agent_email=email%40email.com'
    ```

* Полное совпадение по переданным параметрам (формат даты `dd.mm.YYYY`) - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?address=Test&ship_date=01.01.2024&agent_phone=%2B79062419744&agent_email=email%40email.com'
    ```

* Полное совпадение с лишним полем `unknown` - ожидается название формы

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?address=Test&ship_date=2024-01-01&agent_phone=%2B79062419744&agent_email=email%40email.com&unknown=value'
    ```

* Полное совпадение по названию полей, но почта не совпадает по типу - ожидается список полей с их типами

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?address=Test&ship_date=2024-01-01&agent_phone=%2B79062419744&agent_email=email%40email'
    ```

* Полное совпадение по типам, но не хватает поля `agent_phone` - ожидается список полей с их типами

    ```curl
    curl --location --request POST 'http://localhost:8000/get_forms?address=Test&ship_date=2024-01-01&agent_email=email%40email.com'
    ```

## Запуск Flake8

```bash
make lint
```

## Запуск mypy

```bash
make typecheck
```

## Разработка
### Форматирование кода
При разработке рекомендуется использовать [black](https://pypi.org/project/black/), чтобы поддерживать чистоту кода и избегать лишних изменений при работе с гитом.<br>
Пример конфигурационного файла для Visual Studio Code `.vscode/settings.json`:
```json
{
    "[python]": {
        "editor.defaultFormatter": "ms-python.black-formatter",
        "editor.formatOnSave": true
    }
}
```

### Git хуки
При разработке рекомендуется использовать [pre-commit](https://pre-commit.com/), чтобы перед формированием МР код был уже подготовленным и поверхностно проверенным (например, через `flake8`)<br><br>
**Для использования должны быть установлены dev-зависимости**

#### Pre-commit хуки
Установка
```bash
poetry run pre-commit install
```
Удаление
```bash
poetry run pre-commit uninstall
```
После установки, при каждом коммите будут отрабатывать хуки из [конфигурационного файла](./src/.pre-commit-config.yaml), предназначенные для коммитов (`stages: [commit]`)

#### Pre-push хуки
Установка
```bash
poetry run pre-commit install --hook-type pre-push
```
Удаление
```bash
poetry run pre-commit uninstall -t pre-push
```
После установки, при каждом пуше будут отрабатывать хуки из [конфигурационного файла](./src/.pre-commit-config.yaml), предназначенные для пушей (`stages: [push]`)

### Make
Для удобного запуска контейнеров, их сборки, запуска тестов и т.п. в проекте есть [Makefile](./Makefile)

Для выполнения инструкции, на примере запуска линтера, нужно выполнить команду
```bash
make lint
```
