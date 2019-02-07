# Use an official Python runtime as a parent image
FROM python:2.7.15-stretch

# RUN pip install Flask==0.10.1
RUN groupadd -r uwsgi && useradd -r -g uwsgi uwsgi
RUN pip install Flask==1.0.2 uWSGI==2.0.17 requests==2.5.1 redis==2.10.3 # Flask==0.10.1 uWSGI==2.0.8
WORKDIR /app
COPY app /app
COPY cmd.sh /

EXPOSE 9090 9191

USER uwsgi

# CMD ["python", "identidock.py"]
# CMD ["uwsgi", "--http", "0.0.0.0:9090", "--wsgi-file", "/app/identidock.py", "--callable", "app", "--stats", "0.0.0.0:9191"  ]
CMD ["/cmd.sh"]