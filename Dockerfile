
FROM python:3.9-slim-buster

# # Add a new user "john" with user id 8877
# RUN useradd -u 8877 chof64
# # Change to non-root privilege
# USER chof64

WORKDIR /main

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY . .

# run as non-root
CMD ["python3", "./src/main.py"]
