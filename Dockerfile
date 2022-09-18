FROM python:3.10

WORKDIR /app

RUN pip install --upgrade pipenv

COPY ./Pipfile /app/Pipfile
COPY ./Pipfile.lock /app/Pipfile.lock

RUN pipenv sync

EXPOSE 8080

COPY ./ /app

CMD pipenv run gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:80
