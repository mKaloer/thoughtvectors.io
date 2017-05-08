FROM ubuntu:16.04

MAINTAINER Mads Kalør "mads@kaloer.com"

RUN apt-get update -y
RUN apt-get install -y python3-pip python3-dev

# For Jekyll build tool
RUN apt-get install -y ruby-full git
RUN gem install jekyll bundler

RUN git clone https://github.com/mKaloer/thoughtvectors.io.git jekyll_git

CMD nohup bash -c "./api-server/jekyll_deploy_check.sh &"

COPY ./requirements.txt /api-server/requirements.txt

WORKDIR /api-server

RUN pip3 install -r requirements.txt

COPY . /api-server

CMD uwsgi --ini /api-server/uwsgi.ini