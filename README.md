# FoodGram

FoodGram - "Product Assistant"
On this service, users will be able to publish recipes, subscribe to publications of other users, add their favorite recipes to the "Favorites" list, and before going to the store, download a summary list of products needed to prepare one or more selected dishes.

![](https://github.com/afoninsb/foodgram-project-react/actions/workflows/yamdb_workflow.yml/badge.svg)

[Demo](http://158.160.10.11)

## Environment Variables

To run this project, you will need to add the following environment variables to your .env file

```bash
SECRET_KEY="django-insecure-dfdsfsdsfvohd;vn8e6t345dfgshijlgv_oem#$t8wsds&sz"

DB_ENGINE=django.db.backends.postgresql
POSTGRES_DB=postgres_db
POSTGRES_USER=postgres_user
POSTGRES_PASSWORD=postgres_pass
DB_HOST=db
DB_PORT=5432
```

## Run Locally

Clone the project

```bash
  git clone git@github.com:afoninsb/foodgram-project-react.git
```

Go to the '/infra/' in the project directory and up docker-compose

```bash
  cd my-project/infra
  sudo docker-compose up -d --build
```

In another terminal window
```bash
  cd my-project/infra
  sh run.sh
```
The following will happen:
  - collect static
  - run migrations
  - load test data
  - a superuser will be created

Go to the http://localhost/

API docs can be viewed here - http://localhost/api/docs/redoc.html


## Request examples
### List of recipes
```bash
http://localhost/api/recipes/
```
Response
```bash
{
    "count": 123,
    "next": "http://foodgram.example.org/api/recipes/?page=4",
    "previous": "http://foodgram.example.org/api/recipes/?page=2",
    "results": [
        {
            "id": 0,
            "tags": [],
            "author": {},
            "ingredients": [],
            "is_favorited": true,
            "is_in_shopping_cart": true,
            "name": "string",
            "image": "http://foodgram.example.org/media/recipes/images/image.jpeg",
            "text": "string",
            "cooking_time": 1
        }
    ]
}
```
### User registration
```bash
http://localhost/api/users/
```
Payload
```bash
{
    "email": "vpupkin@yandex.ru",
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин",
    "password": "Qwerty123"
}
```
Response
```bash
{
    "email": "vpupkin@yandex.ru",
    "id": 0,
    "username": "vasya.pupkin",
    "first_name": "Вася",
    "last_name": "Пупкин"
}
```
