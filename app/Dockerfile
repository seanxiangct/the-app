# For more information, please refer to https://aka.ms/vscode-docker-python
FROM python:3.10

WORKDIR /app

# Install dependencies first to speed up the build process
COPY ./requirements.txt /app/requirements.txt
RUN pip install -r requirements.txt

COPY . /app

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE=1

# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED=1

# copy database migrations
COPY migrations .
# COPY aerich.ini .
COPY pyproject.toml .

# Creates a non-root user with an explicit UID and adds permission to access the /app folder
# For more info, please refer to https://aka.ms/vscode-docker-python-configure-containers
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser

# During debugging, this entry point will be overridden. For more information, please refer to https://aka.ms/vscode-docker-python-debug
CMD ["gunicorn", "--bind", "0.0.0.0:5001", "-k", "uvicorn.workers.UvicornWorker", "main:app"]
