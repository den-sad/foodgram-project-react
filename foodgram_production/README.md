# Дипломный проект Foodgram (Сатчин Денис)

## Что нужно сделать для запуска проекта
Скопируйте папку foodgram_production  любым доступным способом на сервер

Остальные действия выполняются на сервере


Перейти в каталог foodgramm

```
cd foodgram_production
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
фронтэнд - http://localhost

api - http://localhost/api

admin панель - http://localhost/admin

документация api - http://localhost/api/docs/
