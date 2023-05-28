# Pull base image
FROM python:3.10.11-alpine

RUN apk add build-base postgresql-client postgresql-dev

# Set environment variables
ENV PIP_DISABLE_PIP_VERSION_CHECK 1
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /var/www/geodjango

# Install dependencies
RUN pip install -U pip
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# Copy project
COPY . .