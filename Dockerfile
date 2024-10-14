FROM python:3.12

RUN apt-get update &&  \
    apt-get install -y python3-dev pip &&  \
    pip install --upgrade pip &&  \
    pip install poetry==1.8.3
COPY ./poetry.lock .
COPY ./pyproject.toml .
RUN poetry config virtualenvs.create false --local && poetry install

COPY ./ /weather_bot/

WORKDIR weather_bot/
ENV PYTHONPATH="/weather_bot:${PYTHONPATH}"

ENTRYPOINT ["python", "main.py"]
