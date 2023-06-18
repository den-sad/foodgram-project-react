# Дипломный проект Foodgram (Сатчин Денис)

## Что нужно сделать для запуска проекта

Перейти в каталог infra

```
cd infra
```

Запустить docker

```
docker compose up --build
```

В контейнере backend выполнить команды:
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
