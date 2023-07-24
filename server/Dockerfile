FROM python:3.11-slim

# Allow statements and log messages to immediately appear in the Cloud Run logs
ENV PYTHONUNBUFFERED 1

RUN pip install poetry

# Create and change to the app directory.
WORKDIR /usr/src/app

COPY . ./

RUN poetry install --no-root
CMD poetry run python -m uvicorn main:app