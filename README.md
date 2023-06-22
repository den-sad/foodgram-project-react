# Дипломный проект Foodgram (Сатчин Денис)
https://foodgram.virtual-it.ru

Данные для тестового доступа
```
суперпользователь  super@super.ru пароль Qverty1

пользователь1 den@den.ru    пароль Qverty1
пользователь2 den2@mail.ru  пароль Qverty1
```

## Что нужно сделать для запуска проекта на локальном хосте
Склонируйте проект

Создайте файл переменных окружения 

```
nano .env
```

Пример содержания
```
SECRET_KEY = 'django-insecure-%t@469cl1%uyh(^vm#de(=a(k$7xcn##9p)e@c75o-*k56h+p6'
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password

DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
```

Перейти в каталог infra

```
cd infra
```

Запустить docker

```
docker compose up --build
```

В контейнере backend выполнить команды:
Миграции
```
docker compose exec backend python manage.py migrate
```

Создание суперпользователя
```
docker compose exec backend python manage.py createsuperuser
```

Создание базовых тэгов (если необходимо)
```
docker compose exec backend python manage.py load_data_to_model Tags
```

Загрузка ингредиентов (если необходимо)
```
docker compose cp ../data backend:/app
docker compose exec backend python manage.py load_data_to_model Ingredients --file ./data/ingredients.json
```

## сайт доступен по адресам:
фронтэнд - http://localhost

api - http://localhost/api

admin панель - http://localhost/admin

документация api - http://localhost/api/docs/


## Что нужно сделать для запуска проекта на сервере
Скопируйте папку foodgram_production  любым доступным способом на сервер

Остальные действия выполняются на сервере


Перейти в каталог foodgram_production

```
cd foodgram_production
```

Создайте файл переменных окружения 

```
nano .env
```

Пример содержания
```
SECRET_KEY = 'django-insecure-%t@469cl1%uyh(^vm#de(=a(k$7xcn##9p)e@c75o-*k56h+p6'
POSTGRES_DB=foodgram
POSTGRES_USER=foodgram_user
POSTGRES_PASSWORD=foodgram_password

DB_NAME=foodgram
DB_HOST=db
DB_PORT=5432
```

Запустить docker

```
docker compose up 
```

В контейнере backend выполнить команды:
Миграции
```
docker compose exec backend python manage.py migrate
```

Создание суперпользователя
```
docker compose exec backend python manage.py createsuperuser
```

Создание базовых тэгов (если необходимо)
```
docker compose exec backend python manage.py load_data_to_model Tags
```

Загрузка ингредиентов (если необходимо)
```
docker compose cp ./data backend:/app
docker compose exec backend python manage.py load_data_to_model Ingredients --file ./data/ingredients.json
```

## сайт доступен по адресам:
фронтэнд - http://site

api - http://site/api

admin панель - http://site/admin

документация api - http://site/api/docs/