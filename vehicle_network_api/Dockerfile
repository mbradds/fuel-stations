FROM python:3.8-slim-buster

ENV FLASK_APP=api.py
ENV LISTEN_PORT=5000
EXPOSE 5000

WORKDIR /app

# Create the environment:
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

# Copy all the python files
COPY . .


# The code to run when container is started:
CMD [ "python3", "-m" , "flask", "run", "--host=0.0.0.0"]