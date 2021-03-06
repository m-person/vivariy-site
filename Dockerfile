# vivariy site
# production environment: django + uwsgi + nginx + supervisor

FROM python:3.6

ENV DEBIAN_FRONTEND noninteractive
ENV PYTHONUNBUFFERED 1

##RUN apt-get update
##RUN apt-get install -y postgresql-client libpq-dev gcc python-pip python-dev libyaml-dev nginx supervisor\
## --no-install-recommends && apt-get clean

RUN apt-get update
RUN apt-get install -y nginx supervisor --no-install-recommends && apt-get clean

RUN mkdir /www
WORKDIR /www

ADD ./requirements.txt /www/requirements.txt
#  RUN pip install supervisor
#RUN pip install supervisor-stdout
RUN pip install uwsgi
RUN pip install -r requirements.txt

ADD . /www

RUN echo "daemon off;" >> /etc/nginx/nginx.conf
RUN rm /etc/nginx/sites-enabled/default
RUN cp deploy/nginx-app.conf /etc/nginx/sites-enabled/
RUN cp deploy/supervisor-app.conf /etc/supervisor/conf.d/
RUN cp deploy/prod_settings.py /www/vivariy_site/

VOLUME ["/www/media", "/www/backups"]

RUN python manage.py collectstatic --noinput

EXPOSE 8001

CMD ["supervisord", "-n"]
#CMD ["/usr/local/bin/uwsgi", "--ini", "/www/deploy/uwsgi.ini"]

