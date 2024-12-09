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
* [Запуск flake8](#запуск-flake8)
    * [Внутри Docker-контейнера (рекомендуется)](#внутри-docker-контейнера-рекомендуется-1)
    * [Вне Docker-контейнера](#вне-docker-контейнера-1)
* [Запуск mypy](#запуск-mypy)
    * [Внутри Docker-контейнера (рекомендуется)](#внутри-docker-контейнера-рекомендуется-2)
    * [Вне Docker-контейнера](#вне-docker-контейнера-2)
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

#### ENVIRONMENT
Окружение (development, production, testing, etc). Может быть использовано для различных нужд в рамках проекта
#### PROJECT_NAME
Название проекта
#### SECRET_KEY
Секретный ключ для FastAPI
#### DEBUG
Режим отладки<br>
0 - выключен<br>
1 - включен<br>
Если включен, то:
* 500 ошибки сервера не будут обработаны обработчиком исключений
#### PROD
Режим прод окружения<br>
0 - выключен<br>
1 - включен<br>
#### MEDIA_PATH
Путь к директории, в которой хранятся медиа-файлы
#### MEDIA_URL
Префикс в ссылке для медиа-файлов
#### STATIC_PATH
Путь к директории, в которой хранятся статические файлы
#### STATIC_URL
Префикс в ссылке для статических-файлов
#### LOG_PATH
Путь к директории, в которой хранятся лог-файлы
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

### Запуск в локальном окружении
```bash
docker compose -f docker/docker-compose.yml -f docker/docker-compose.local.yml up
```
или
```bash
make localup
```
После запуска проект будет доступен по адресу http://localhost:${NGINX_OUTER_PORT}/
### Запуск в тестовом окружении
```bash
docker compose up
```
или
```bash
make up
```
### После запуска
Проект станет доступен по порту ${NGINX_OUTER_PORT}<br>
В локальном окружении достаточно перейти по адресу http://localhost:${NGINX_OUTER_PORT}/<br>
В другом окружении необходимо настроить домен, при обращении к которому веб-сервер (Nginx/Apache) будет проксировать все запросы на порт ${NGINX_OUTER_PORT}

## Запуск Flake8
### Внутри Docker-контейнера (рекомендуется)

1. Зайти в контейнер `asgi` через команду

    ```bash
    docker exec -it ${PROJECT_NAME}-asgi bash
    ```
2. Начать выполнение flake8 через команду
    ```bash
    flake8 .
    ```

или
```bash
make lint
```

### Вне Docker-контейнера

1. Перейти в директорию с [конфигурационным файлом](./src/.flake8)
2. Начать выполнение flake8 через команду

    ```bash
    poetry run flake8 .
    ```

## Запуск mypy
### Внутри Docker-контейнера (рекомендуется)

1. Зайти в контейнер `asgi` через команду

    ```bash
    docker exec -it ${PROJECT_NAME}-asgi bash
    ```
2. Начать выполнение mypy через команду
    ```bash
    mypy .
    ```

или
```bash
make typecheck
```

### Вне Docker-контейнера

При возникновении ошибок запуск возможен только внутри Docker-контейнера
1. Перейти в директорию с [конфигурационным файлом](./src/pyproject.toml)
2. Начать выполнение mypy через команду

    ```bash
    poetry run mypy .
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
