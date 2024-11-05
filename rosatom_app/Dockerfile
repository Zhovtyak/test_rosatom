FROM python:3.13

WORKDIR /app

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV PYTHONPATH=${pwd}
ENV DJANGO_SETTINGS_MODULE=rosatom_app.settings

CMD ["pytest"]