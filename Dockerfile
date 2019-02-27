FROM python:3

WORKDIR /app

COPY requirements.txt requirements.txt
RUN python -m pip install -r requirements.txt

COPY . .

ENV DJANGO_SU_NAME=admin
ENV DJANGO_SU_PASSWORD=admin

EXPOSE 8000

CMD [ "python", "./run.py", "0.0.0.0:8000" ]
