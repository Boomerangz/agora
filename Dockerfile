FROM python:3
RUN mkdir /code
WORKDIR /code
COPY requirements.txt /code/
RUN pip install -r requirements.txt
COPY . /code/
EXPOSE 8000
CMD python /code/manage.py migrate && /code/manage.py runserver 0.0.0.0:8000
