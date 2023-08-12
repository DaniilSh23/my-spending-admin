FROM python:3.10-slim

RUN mkdir "my_spending_admin"

COPY requirements.txt /my_spending_admin/

RUN apt update

RUN apt install python3-dev libpq-dev postgresql-contrib curl -y

RUN apt-get install build-essential -y

RUN pip install psycopg2-binary

RUN python -m pip install --no-cache-dir -r /my_spending_admin/requirements.txt

COPY . /my_spending_admin/

WORKDIR /my_spending_admin

# Ниже команды для создания суперпользователя в Django
ENV DJANGO_SUPERUSER_USERNAME=admin
ENV DJANGO_SUPERUSER_PASSWORD=admin
ENV DJANGO_SUPERUSER_EMAIL=my@dmin.com

# Открываем 8000 порт
EXPOSE 8000

# Запуск
ENTRYPOINT ["/my_spending_admin/entrypoint.sh"]