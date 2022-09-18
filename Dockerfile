FROM kennethreitz/pipenv:latest

WORKDIR app/

EXPOSE 8080

COPY . .
CMD gunicorn main:app --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8080
