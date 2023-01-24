# praktikum_new_diplom

Создам хороший файл, когда полностью доделаю проект

1. Открыть терминал в папке infra
2. Дать команду
```
sudo docker-compose up --build
```
3. Когда всё запустится, открыть второй терминал в папке infra
4. Дать команду
```
sh run.sh
```
При этом произойдёт следующее:
 - соберётся статика
 - выполнятся миграции
 - загрузятся тестовые данные
 - создастся суперпользователь - надо будет ввести его данные

Информация о тестовых пользователях:
{
"email": "kolya@kolya.ru",
"username": "kolya",
"first_name": "kolya",
"last_name": "kolyaev",
"password": "Fgtkmcby1"
}
d1d7a852e59c22774b5add39d8e69b0a42a9f5ee

{
"email": "vasya@vasya.ru",
"username": "vasya",
"first_name": "vasya",
"last_name": "vasiliev",
"password": "Fgtkmcby1"
}
ab3b9f8e7c50f1397e91cd7f4079edc59f5cc614

Рецепты без картинок, т.к. тестовые данные создавал в докере, и фотки там внутри.
Как их оттуда передать тебе, не знаю.
