# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.7-slim

WORKDIR /app

COPY . /app

# EXPOSE 8080

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
ADD requirements.txt .
# RUN python -m pip install --upgrade pip && python -m pip install -r requirements.txt 

RUN apt-get update && apt-get install -y libgomp1

RUN pip install --trusted-host pypi.python.org -r requirements.txt


# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
# CMD ["python", "app.py"]
#  --threads 4 --timeout 120 -k gevent
# --workers 4 --timeout 120
CMD exec gunicorn --bind :$PORT --workers 2 --timeout 120 app:app
