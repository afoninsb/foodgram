#!/bin/sh
echo "##### НАЧИНАЕМ РАБОТУ #####"
echo "### 1. Собираем статику ###"
sudo docker-compose exec web python manage.py collectstatic --no-input
echo "### 2. Выполняем миграции ###"
sudo docker-compose exec web python3 manage.py migrate
echo "??? 3. Будем загружать тестовые данные? ('Д/н' или 'Y/n' ) "
read yesno
if [ "$yesno" = "д" ] || [ "$yesno" = "y" ] || [ "$yesno" = "" ] || [ "$yesno" = "Y" ] || [ "$yesno" = "Д" ]
then
	echo "### 3. Загружаем тестовые данные ###"
	sudo docker-compose exec web python3 manage.py loaddata dump.json
fi
echo "??? 4. Будем создавать суперпользователя? ('Д/н' или 'Y/n' ) "
read  yesno
if [ "$yesno" = "д" ] || [ "$yesno" = "y" ] || [ "$yesno" = "" ] || [ "$yesno" = "Y" ] || [ "$yesno" = "Д" ]
then
	echo "### 4. Создаём суперпользователя ###"
	sudo docker-compose exec web python3 manage.py createsuperuser
fi
echo "##### РАБОТА ЗАВЕРШЕНА #####"
