FROM python:3.11

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /usr/src/app

RUN apt-get update && apt-get upgrade -y
RUN apt-get install postgresql postgresql-contrib gcc -y

#COPY ./config/requirements.txt /usr/src/app
RUN pip install --upgrade pip
COPY ./requirements/* /usr/src/app/requirements/
RUN pip install -r requirements/local.txt

# copy entrypoint.sh
COPY ./entrypoint.sh /usr/src/app/
RUN sed -i 's/\r$//g' /usr/src/app/entrypoint.sh
RUN chmod +x /usr/src/app/entrypoint.sh

COPY . /usr/src/app

ENTRYPOINT ["/usr/src/app/entrypoint.sh"]
