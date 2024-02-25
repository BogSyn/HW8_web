# Домашнє завдання #8

<h1>Перша частина:</h1>

    HW8/part_1

<b>Створена база даних Atlas MongoDB:</b>

    файл конфігурації ->    part_1/conf/config.ini

    URI = "mongodb+srv://ravlykplus:qwerty1234@cluster0.hs7dfmm.mongodb.net/hw_8?retryWrites=true&w=majority"

<b>Моделі ODM Mongoengine:</b>

    part_1/seeds/model.py

<b>Скрипт для завантаження в json файлів в базу даних:</b>

    part_1/seeds/seed.py

<b>Для кешування запустити контейнер:</b>

    docker run --name redis-cache -d -p 6379:6379 redis

<b>Скрипт для пошуку цитат за тегом та ім'ям автора:</b>

    part_1/main.py

Приклад:

`name: Steve Martin` — знайти та повернути список всіх цитат автора `Steve Martin`;
`tag:life` — знайти та повернути список цитат для тега `life`;
`tags:life,live` — знайти та повернути список цитат, де є теги `lif`e або `live` (примітка: без пробілів між тегами `life, live`);
`exit` — завершити виконання скрипту;

Для команд `name:Steve Martin` та `tag:life` реалізована можливість скороченого запису значень для пошуку, як name:`st` та `tag:li` відповідно;


<h1>Друга частина:</h1>

    HW8/part_2

<b>Контейнер RabbitMQ:</b>

    docker run -d --name rabbitmq_hw8 -p 5672:5672 -p 15672:15672 rabbitmq:3.13-management

<h1>Опис:</h1>

База даних використана з першої частини домашнього завдання, створюється колекція `contacts`.

Моделі ODM Mongoengine:

    part_2/models.py

`producer.py` генерує 20 фейкових контактів та записує їх у базу даних. Потім поміщає у дві черги `['email_queue', 'sms_queue']` RabbitMQ

`consumer_sms.py` та `consumer_email.py` обробляються кожен свою чергу і оновлюють `sms_sent` та `email_sent` на `True`, кожен своє, в базі даних.