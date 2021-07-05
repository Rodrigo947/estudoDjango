FROM python:3.9

ARG TYPE_ENV

WORKDIR /code

COPY . /code

RUN pip install pipenv

RUN if [ "$TYPE_ENV" = "dev" ]; then \
  pipenv install --dev --system --deploy; \
  else \
  pipenv install --system --deploy; \
  fi

ENTRYPOINT ["sh", "entrypoint.sh"]