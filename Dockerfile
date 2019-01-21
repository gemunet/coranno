FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .

RUN python manage.py makemigrations
RUN python manage.py migrate --noinput

ENV DJANGO_DB_NAME=default
ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_EMAIL=
ENV DJANGO_SU_PASSWORD=admin

RUN python -c "import os; os.environ['DJANGO_SETTINGS_MODULE'] = 'coranno.settings'; \
   import django; django.setup(); \
   from django.contrib.auth.management.commands.createsuperuser import get_user_model; \
   get_user_model()._default_manager.db_manager('$DJANGO_DB_NAME').create_superuser( \
   username='$DJANGO_SU_NAME', \
   email='$DJANGO_SU_EMAIL', \
   password='$DJANGO_SU_PASSWORD')"

EXPOSE 8000

CMD [ "python", "./manage.py", "runserver", "0.0.0.0:8000" ]
