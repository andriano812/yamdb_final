# API_YaMDb

## О проекте
REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке. YaMDb 
собирает отзывы (Review) пользователей на произведения (Titles). 

Произведения делятся на категории: «Книги», «Фильмы», «Музыка». 
Список категорий (Category) может быть расширен администратором.

Произведению может быть присвоен один или несколько жанров (Genre) из списка
предустановленных. Новые жанры может создавать только администратор.

Читатели оставляют к произведениям текстовые отзывы и выставляют рейтинг
(оценку в диапазоне от одного до десяти). Из множества оценок автоматически 
определяется средняя оценка произведения.

## Развертывание

1 шаг. Создать и заполнить по образцу .env:

```sh
DB_ENGINE=None
DB_NAME=None
POSTGRES_USER=None
POSTGRES_PASSWORD=None
DB_HOST=None
DB_PORT=None
```

2 шаг. Собрать и запустить контейнер:

```sh
docker-compose up -d --build 
```

3 шаг. Выполнить миграции:

```sh
docker-compose exec web python manage.py migrate
```

4 шаг. Собрать статики:

```sh
docker-compose exec web python manage.py collectstatic --no-input
```

## Создание superuser

```sh
docker-compose exec web python manage.py createsuperuser
```

## Заполнение базы стартовыми данными

```sh
docker-compose exec web python manage.py loaddata fixtures.json
```

## Бейдж

![example workflow](https://github.com/andriano812/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

## Адрес для проверки:

http://62.84.121.111/admin/
http://62.84.121.111/redoc/
http://62.84.121.111/api/v1/genres/

## Автор

- *Андрей Пустобаев*