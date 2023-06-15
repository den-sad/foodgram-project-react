
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN apt update -y
RUN apt install libpq-dev -y
RUN pip install gunicorn==20.1.0 
RUN pip install -r requirements.txt --no-cache-dir
COPY ./app .

RUN python manage.py makemigrations api food users --no-input
RUN python manage.py migrate --no-input
RUN python manage.py collectstatic --no-input


RUN mkdir collected_static
RUN mkdir ./collected_static/static
RUN cp -r backend_static/. collected_static/static/.

CMD ["gunicorn", "--bind", "0.0.0.0:8000", "app.wsgi"]