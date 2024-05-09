
<p align="center">
    <img src="backend/data/logo.png" width="150">
</p>

<h1 align="center">Продуктовый помощник</h1>

<p align="center">
    <a href="https://github.com/mxnoob/foodgram/actions?query=workflow:CI/CD">
        <img alt="GitHub - Test status" src="https://github.com/mxnoob/foodgram/actions/workflows/main.yml/badge.svg">
    </a>
    <a href="https://results.pre-commit.ci/latest/github/mxnoob/foodgram/main">
        <img alt="pre-commit.ci status" src="https://results.pre-commit.ci/badge/github/mxnoob/foodgram/main.svg">
    </a>
</p>
<h2 align="center">Стек технологий</h2>

<p align="center">
    <a href="https://www.djangoproject.com/">
        <img alt="Django" src="https://img.shields.io/badge/django-%23092E20.svg?style=for-the-badge&logo=django&logoColor=white">
    </a>
    <a href="https://www.django-rest-framework.org/">
        <img alt="Django-REST-Framework" src="https://img.shields.io/badge/DJANGO-REST-ff1709?style=for-the-badge&logo=django&logoColor=white&color=ff1709&labelColor=gray">
    </a>
    <a href="https://www.postgresql.org/">
        <img alt="PostgreSQL" src="https://img.shields.io/badge/postgres-%23316192.svg?style=for-the-badge&logo=postgresql&logoColor=white">
    </a>
    <a href="https://nginx.org/ru/">
        <img alt="Nginx" src="https://img.shields.io/badge/nginx-%23009639.svg?style=for-the-badge&logo=nginx&logoColor=white">
    </a>
    <a href="https://gunicorn.org/">
        <img alt="gunicorn" src="https://img.shields.io/badge/gunicorn-%298729.svg?style=for-the-badge&logo=gunicorn&logoColor=white">
    </a>
    <a href="https://www.docker.com/">
        <img alt="docker" src="https://img.shields.io/badge/docker-%230db7ed.svg?style=for-the-badge&logo=docker&logoColor=white">
    </a>
</p>
<h2 align="center">Описание</h2>

<p>
    Foodgram - приложение, с помощью которого, пользователи могут создавать рецепты, добавлять в избраное, создавать список покупок и подписываться на авторов рецептов.</p>
    <p>В списке покупок можно скачать `.pdf` файл, который включает в себя список ингредиентов и названия рецептов.
</p>

<h3 align="center">
    <a href="http://foodgrm.hopto.org">Пример сайта</a><p></p>
    <a href="http://foodgrm.hopto.org/api/docs/">Документация</a>
</h3>


<h2 align="center">Запуск</h2>

```shell
# Склонировать репозиторий
git clone git@github.com:mxnoob/foodgram.git
```

> [!IMPORTANT]
> Необходимо создать файл `.env` с переменными окружения в папке `infra`.</br>
> Пример файла [infra/.env.example](https://github.com/mxnoob/foodgram/blob/6144c03a787cb75549b26c2059937192cce50b0a/infra/.env.example#L1-L13)


```shell
# Запустить докер композ
docker compose -f infra/docker-local.yml up -d --build
```
## Как наполнить БД данными

```bash
# Добавить теги
docker compose -f infra/docker-local.yml python manage.py add_tags
# Добавить ингредиенты
docker compose -f infra/docker-local.yml python manage.py add_ingredients
```


## Пример запросов/ответов

#### Get all items

```http
  GET /api/recipes/
```

| Parameter | Type     | Description                                                            |
| :-------- | :------- |:-----------------------------------------------------------------------|
| `page` | `integer` | Номер страницы.                                                        |
| `limit` | `integer` | Количество объектов на странице.                                       |
| `is_favorited` | `integer` | Enum: `0` `1`. Показывать только рецепты, находящиеся в списке избранного. |
| `is_in_shopping_cart` | `integer` | Enum: `0` `1`. Показывать только рецепты, находящиеся в списке покупок. |
| `author` | `integer` | Показывать рецепты только автора с указанным id.                                                        |
| `tags` | `Array of strings` | xample: `tags=lunch&tags=breakfast`. Показывать рецепты только с указанными тегами (по slug)                                            |

#### Get item

```http
  GET /api/recipes/{id}/
```

| Parameter | Type     | Description                                            |
| :-------- | :------- |:-------------------------------------------------------|
| `id`      | `string` | **Required**. Уникальный идентификатор этого рецепта  |

## Автор:

[mxnoob](https://www.github.com/mxnoob)