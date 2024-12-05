# syntax=docker/dockerfile:1

# Comments are provided throughout this file to help you get started.
# If you need more help, visit the Dockerfile reference guide at
# https://docs.docker.com/go/dockerfile-reference/

# Want to help us make this template better? Share your feedback here: https://forms.gle/ybq9Krt8jtBL3iCk7
FROM python:2.7-buster

RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 0E98404D386FA1D9
RUN apt-key adv --keyserver keyserver.ubuntu.com --recv-keys 6ED0E7B82643E131
RUN echo "deb http://archive.debian.org/debian buster-backports main contrib non-free" | tee -a /etc/apt/sources.list
RUN apt-get update
RUN apt-get upgrade -y
RUN apt-get install -t buster-backports gdal-bin libgdal-dev python-gdal libgeos-dev -y

RUN apt-get install -y --no-install-recommends \
    build-essential \
    python-pip \
    postgresql-client \
    ruby-sass \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Prevents Python from writing pyc files.
ENV PYTHONDONTWRITEBYTECODE=1

# Keeps Python from buffering stdout and stderr to avoid situations where
# the application crashes without emitting any logs due to buffering.
ENV PYTHONUNBUFFERED=1

WORKDIR /app

# Create a non-privileged user that the app will run under.
# See https://docs.docker.com/go/dockerfile-user-best-practices/
ARG UID=10001
RUN adduser \
    --disabled-password \
    --gecos "" \
    --home "/tmp" \
    --shell "/sbin/nologin" \
    --no-create-home \
    --uid "${UID}" \
    appuser

# Download dependencies as a separate step to take advantage of Docker's caching.
# Leverage a cache mount to /root/.cache/pip to speed up subsequent builds.
# Leverage a bind mount to requirements.txt to avoid having to copy them into
# into this layer.
COPY . .
RUN pip install --upgrade pip
RUN python -m pip install -r requirements.txt

# Switch to the non-privileged user to run the application.
USER appuser

# Copy the source code into the container.

# Expose the port that the application listens on.
EXPOSE 8000

# Run the application.
CMD python manage.py runserver 0.0.0.0:8000
