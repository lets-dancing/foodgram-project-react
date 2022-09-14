# praktikum_new_diplom
[![Django-app workflow](https://github.com/lets-dancing/foodgram-project-react/actions/workflows/foodgram_workflow.yml/badge.svg?branch=master)](https://github.com/lets-dancing/foodgram-project-react/actions/workflows/foodgram_workflow.yml)

http://recipe.sytes.net/recipes

## Разворачивание проекта на сервере:

1. **Необходимые условия и замечания:**
    * Проект работает в связке контейнеров Docker. Минимальная версия Docker-compose - 3
    * Перед этапом эксплуатации необходим подготовительный этап.
    * Схема модернизации и сопровождения проекта включает в себя репозиторий на GitHub, создание и хранение образов частей проекта на DockerHub посредством подсистемы workflow GitHub-actions.
    * Перед запуском проекта на продакш-сервере соответствующие образы должны быть сформированы на DockerHub. Сборка и размещение на DockerHub образов описаны в разделе "build_and_push_to_docker_hub" файла "/.github/workflows/foodgram_workflow.yml".


2. **Последовательный план действий.**
    * Создать на удалённом сервере папку для проекта, например "foodgramm-react".
    * Скопировать в эту папку содержимое папки "infra".
    * В папке "infra" с именем ".env" и наполнить его следующими данными:
    ```
    SECRET_KEY='секретный ключ Django'
    POSTGRES_DB=имя_базы_данных
    POSTGRES_USER=логин_в_бд
    POSTGRES_PASSWORD=пароль_в_бд
    DB_HOST=db  # имя контейнера БД, должно совпадать с тем, что прописано в сценариях Docker-а
    DB_PORT=5432
    DEBUG=TRUE
    ALLOWED_HOSTS=* backend localhost 127.0.0.1  # имена/IP хостов через пробел
    ```
    * В файле "docker-compose.yml" указать свои имена образов на DockerHub.
    * Скопировать папку "docs" из корня данного репозитория в папку проекта на удалённом сервере для доступа к документации API или исключить(закомментировать) настройки этой папки в файле "docker-compose.yml".
    * Скопировать папку "data" из корня данного репозитория в папку проекта на удалённом сервере для возможности подгрузки в БД сервера заготовок фикстур к моделям продуктов и тегов.
    * Находясь в папке проекта запустить первоначальную инициализацию:
        ```bash
        docker-compose up --build -d
        ```
    _Первоначальная сборка контейнеров из образов может занять заметное время._
    * После удачного запуска объединения из трёх контейнеров проекта
        * необходимо:
            * инициализировать БД. В терминах Django - применить миграции:
            ```bash
            sudo docker exec infra_web_1 python manage.py migrate
            ```
            * создать суперпользователя:

            ```bash
            sudo docker exec infra_web_1 python manage.py createsuperuser
            ```
        * необязательно, но полезно(отображение административных страниц в удобном формате значительно упрощает наглядность сопровождения проекта):
            * собрать статику:
            ```bash
            sudo docker exec infra_web_1 python manage.py collectstatic
            ```
        * необязательно, но возможно:
            * загрузить заготовку БД для таблиц тегов и продуктов. Имена таблиц и файлов прописаны в коде management-команды.
            ```bash
            sudo docker exec infra_web_1 python manage.py load_data
            ```
    * Дальнейшая работа по развёртыванию доработок проекта автоматизирована механизмом GiHub-actions. На текущий момент workflow отлеживает событие "push" в ветку "master".
    
3. **Необходимые для запуска проекта переменные для Gihub-actions:**
    * относящиеся к Dockerhub:
        * DOCKER_USERNAME
        * DOCKER_PASSWORD
        
        
        _соответственно, логин и пароль на DockerHub. В workflow имена образов для Dockerhub прописаны в коде, можно также заменить на конфигурируемые через секреты._

    * относящиеся к удалённому серверу(production):
        * HOST
        * USER
        * SSH_KEY
        * PASSPHRASE
        * PROJECT_FOLDER


        _используются в workflow для логина на сервер и перехода в папку проекта_
    * относящиеся к настройкам кода backend-а и сценариев сборки образов Docker:
        * ALLOWED_HOSTS
        * SECRET_KEY
        * DEBUG
        * DB_ENGINE
        * DB_HOST
        * DB_NAME
        * DB_PORT        
        * POSTGRES_PASSWORD        
        * POSTGRES_USER


        _используются в workflow для генерации файла "**.env**" в папке проекта, а также значения используются в контейнере "**infra_web_1**" для инициализации и работы django-проекта через его "**settings.py**". Для ALLOWED_HOSTS несколько значений указываются через пробел. Значения DB_NAME, POSTGRES_USER и POSTGRES_PASSWORD также используются в контейнере "**db**" для инициализации БД PostgreSQL._
    * для отсылки сообщения в Телеграм на завершающем этапе workflow:
        * TELEGRAM_TO  - ID телеграм-аккаунта того, кому будет послано сообщение.
Узнать свой ID можно у бота @userinfobot.
        * TELEGRAM_TOKEN - токен бота, созданного тем, кому будет послано сообщение.
Получить этот токен можно у бота @BotFather.
