FROM python:3.11.8-slim-bookworm AS requirements-stage

WORKDIR /tmp

RUN pip install --no-cache-dir poetry==1.8.2

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export --without=dev -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.11.8-slim-bookworm

ARG GIT_REVISION="0000000"
ARG GIT_TAG="x.x.x"

WORKDIR /app

COPY --from=requirements-stage /tmp/requirements.txt /app/requirements.txt
COPY . .

# Install packages: https://stackoverflow.com/a/68666500/4457856
RUN apt-get update \
    && apt-get install -y ffmpeg libsm6 libxext6

# Install dependencies
RUN pip install --no-cache-dir --upgrade -r /app/requirements.txt

CMD ["python", "-m", "streamlit", "run", "apps/99_streamlit_examples/main.py"]
