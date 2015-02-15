FROM dockerfile/ubuntu
MAINTAINER Ashar Rizqi <asharrizqi@gmail.com>

#add to repo list
run echo "deb http://archive.ubuntu.com/ubuntu precise main universe" >> /etc/apt/sources.list
run apt-get update

#setup tools and python
RUN \
  apt-get install -y tar \
                     git \
                     curl \
                     wget \
                     net-tools \
                     build-essential

RUN \
  apt-get install -y python \
                     python-dev \
                     python-distribute \
                     python-pip

#install flask
RUN \
  pip install flask

#instal uwsgi
RUN \
  pip install uwsgi

#install pandas
RUN \
  pip install pandas

#install xlrd
RUN \
  pip install git+https://github.com/python-excel/xlrd.git


# Install Nginx.
RUN \
  add-apt-repository -y ppa:nginx/stable && \
  apt-get update && \
  apt-get install -y nginx && \
  rm -rf /var/lib/apt/lists/*

# symlink conf dir
RUN ln -s /open_data/etc/conf/nginx.conf /etc/nginx/sites-enabled/
RUN unlink /etc/nginx/sites-enabled/default

# Define mountable directories.
VOLUME ["/etc/nginx/sites-enabled", "/etc/nginx/certs", "/etc/nginx/conf.d", "/var/log/nginx"]


# Expose ports.
EXPOSE 80
EXPOSE 443

RUN echo "daemon off;" >> /etc/nginx/nginx.conf

RUN mkdir -p /var/log/uwsgi/
RUN touch /var/log/uwsgi/uwsgi.log

RUN touch /run.sh
RUN chmod 755 /run.sh
RUN echo "#!/bin/bash\nuwsgi --socket 127.0.0.1:8080 --chdir /opendata/ --module app --callable app --processes 1 --daemonize /var/log/uwsgi/uwsgi.log;nginx;" >> /run.sh

CMD ["/run.sh"]

