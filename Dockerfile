
# STAGE 1: Initialization of the base Python environment.
#//---------------------------------------------------------------------------

FROM python:3.9 AS stage-1
RUN apt update && apt install -y curl
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python -
ENV PATH="/root/.poetry/bin:$PATH"


# STAGE 2: Installation of large/independent application dependencies.
#//---------------------------------------------------------------------------

FROM stage-1 AS stage-2
RUN apt update

# RUN apt update && apt install -y wget
# RUN wget -O /tmp/google-chrome-stable_current_amd64.deb https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# RUN apt install -y /tmp/google-chrome-stable_current_amd64.deb
# RUN rm /tmp/google-chrome-stable_current_amd64.deb


# STAGE 3: Installation of application dependencies.
#//---------------------------------------------------------------------------

FROM stage-2 AS stage-3
RUN apt update && apt install -y git
WORKDIR /hecate
COPY pyproject.toml .
COPY poetry.lock .
RUN poetry config virtualenvs.create false
RUN poetry install --no-dev
COPY . .
CMD ["python","./src/main.py"]
