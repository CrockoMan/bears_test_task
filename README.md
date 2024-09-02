## BEARS Тестовое задание Python-разработчик 
Тестовое задание.    </br>
Описание задания https://docs.google.com/document/d/1Sw1HdiJ-yJRoNv3HRlN7RN9ifZbCPFFVOCkqFr4cTT4/edit
### Работоспособность бекенда можно проверить здесь: http://194.26.226.134/  </br></br>
### Работоспособность бота можно проверить здесь: https://t.me/CrockoTeleBot  </br>
##### Стек: Pyton, FastAPI, aiogram, sqlalchemy
При реализации тестового задания, из-за единственного эндпоинта было принято 
решение использовать "облегченные" структуры проектов FastAPI и aiogram. 
Проект разделён на два независимых блока: backend и bot. Проект можно 
запускать как на одной машине, так и разделить на двух отдельных. Бот получает данные от бекенда по api.
Поэтому необходимо реализовать доступность бекенда в сети интернет для корректного 
"общения" бота с бекендом. Для этого можно использовать как станции с 
статическим ip и выходом в интернет c настройкой nginx, так и использовать 
другие методы туннелирования, например ngrok (обратитесь к инструкции https://ngrok.com/docs/).</br></br>

Работа бека:

![image](https://github.com/user-attachments/assets/08e7ca1e-64e2-47f8-a0fa-928287b10d9e)


Периодическое обновление бд:

![image](https://github.com/user-attachments/assets/9e041780-6cce-431b-8282-58b2fab13948)


Работа бота:

![image](https://github.com/user-attachments/assets/b1ee5c18-7695-4fcd-b523-27be1eef1c23)


Запуск проекта:</br>
Клонировать репозиторий и перейти в него в командной строке:

```
git clone git@github.com:CrockoMan/bears_test_task.git
```

```
cd bears_test_task
```

Cоздать и активировать виртуальное окружение:

```
python3 -m venv venv
```

* Если у вас Linux/macOS

    ```
    source venv/bin/activate
    ```

* Если у вас windows

    ```
    source venv/scripts/activate
    ```

Установить зависимости из файла requirements.txt:
* Если у вас Linux/macOS

    ```
    python3 -m pip install --upgrade pip
    pip install -r requirements.txt
    ```
* Если у вас windows

    ```
  python -m pip install --upgrade pip  
  pip install -r requirements.txt
    ```

Заполнить файл конфигурации .env
```
ALLOWED_HOSTS= # Разрешенные хосты и при необходимости порты, например 127.0.0.1:8000,localhost:8000,http://194.26.226.134/

POSTGRES_DB= # имя базы данных
POSTGRES_USER= # имя пользователя БД
POSTGRES_PASSWORD= # пароль БД
DB_HOST= # хост, на котором развернута БД
DB_PORT= # порт БД
UPDATE_PERIOD= # Период обновления записей в БД
HTTP_PREFIX="https://card.wb.ru/cards/v1/detail?appType=1&curr=rub&dest=-1257786&spp=30&nm="

BOT_TOKEN= # Токен телеграм бота
URL_BACKEND = # URL расположения бекенда, например 'http://194.26.226.134/'

```
Для запуска бекенда: Перейти в каталог бекенд и Запустить сервис:

```
cd backend
uvicorn main:app --reload
```

Для запуска бота: Перейти в каталог бота и Запустить сервис:

```
cd bot
python bot.py
```

### API бекенд сервиса доступен после запуска 
[Redoc](http://127.0.0.1:8000/docs/)  http://127.0.0.1:8000/docs  </br>
[Swagger](http://127.0.0.1:8000/redoc/)  http://127.0.0.1:8000/redoc  </br>

Для разворачивания проекта с помощью докер требуется компьютер с предустановленным Docker и Docker-Compose. Инструкция по установке: https://docs.docker.com/  </br>
Сборка Docker-образа  </br>
Перейдите в каталог проекта, где находится Dockerfile соберите запустите контейнер

```
cd backend
docker compose -f docker-compose.yml up
cd bot
docker compose -f docker-compose.yml up
```

Автор: [К.Гурашкин](https://github.com/CrockoMan)
