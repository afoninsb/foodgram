#!/bin/sh
echo "Собираем статику"
sudo docker-compose exec web python manage.py collectstatic --no-input
echo "Выполняем миграции"
sudo docker-compose exec web python3 manage.py migrate
echo "Создаём суперпользователя"
sudo docker-compose exec web python3 manage.py createsuperuser