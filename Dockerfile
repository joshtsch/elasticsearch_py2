FROM python:2.7
MAINTAINER "Josh Tscheschlog" <joshtsch106@gmail.com>

RUN yum update -y && \
    yum install -y python-pip python-dev

RUN pip install --upgrade pip

RUN pip install nose

ENTRYPOINT ["python"]
