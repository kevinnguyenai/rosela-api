FROM python:3.7-slim
ENV APP_HOME /
WORKDIR $APP_HOME
COPY . ./
COPY .env.local .env
RUN pip install -r requirements.txt
RUN alembic upgrade head
CMD exec gunicorn --bind :$PORT --workers 1 --worker-class uvicorn.workers.UvicornWorker  --threads 8 main:app