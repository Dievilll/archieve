FROM python:3.10.6

ENV PYTHONUNBUFFERED=1

WORKDIR /vf_config_archive
COPY req.txt .
RUN pip install -r req.txt
COPY . .

CMD gunicorn api.api:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind=0.0.0.0:9020
