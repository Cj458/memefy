FROM python:3.11

ARG REGISTER
ARG PROJECT_NAME
ARG VERSION
# set work directory
RUN mkdir /app

WORKDIR /app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
#ENV PATH=$PATH:/root/.local/bin

# copy requirements file
COPY requirements.txt /app

RUN pip install --no-cache-dir --upgrade -r requirements.txt
# RUN pip install --no-cache-dir alembic psycopg2

# Copy the entire project into the container
COPY .env /app
COPY . /app



EXPOSE 8000


CMD bash -c 'uvicorn services.web.app.main:app --host 0.0.0.0 --port 8000 --reload'


