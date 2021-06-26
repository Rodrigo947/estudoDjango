FROM python:3.9

WORKDIR /code

COPY . /code

RUN pip install pipenv

RUN pipenv install --dev --system --deploy

ENTRYPOINT ["sh", "entrypoint.sh"]