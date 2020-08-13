FROM python:alpine

RUN mkdir -p /accela
COPY . /accela
RUN pip install -r /accela/requirements.txt
WORKDIR /accela

EXPOSE 80

CMD ["gunicorn", "--config", "gunicorn_config.py", "--chdir","app","accela:app"]
