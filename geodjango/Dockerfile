# Pull base image
FROM ghcr.io/osgeo/gdal:alpine-normal-latest

RUN apk add build-base py3-pip python3-dev libpq-dev

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