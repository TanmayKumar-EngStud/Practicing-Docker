FROM python:3.6 as base
# Base image to be reused
LABEL maintainer "Thiago Pacheco <hi@pacheco.io>"
RUN apt-get update
WORKDIR /usr/src/app
COPY ./flask-api/requirements.txt ./flask-api/requirements.txt 
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install --no-cache-dir -r ./flask-api/requirements.txt
ENV FLASK_ENV="docker"
ENV FLASK_APP=app.py
EXPOSE 5000

FROM base as debug
# Debug image reusing the base
# Install dev dependencies for debugging
RUN pip install debugpy
# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

FROM base as prod
# Production image
RUN pip install gunicorn
COPY . .
CMD ["gunicorn", "--reload", "--bind", "0.0.0.0:5000", "app:app"]