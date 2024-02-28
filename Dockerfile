FROM docker.io/library/python:3.8

# Set the working directory in the container
WORKDIR /app

COPY requirements.txt /app/
RUN pip install -r requirements.txt

CMD [ "python", "main.py" ]
