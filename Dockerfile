FROM python:2.7
MAINTAINER "Josh Tscheschlog" <joshtsch106@gmail.com>

RUN pip install nose

ENTRYPOINT ["python"]
