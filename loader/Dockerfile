# Use an official Python runtime as a parent image
FROM python:3.11

# Set the working directory to /app
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

## Install system deps
RUN pip install --upgrade pip && \
    pip install --trusted-host pypi.python.org poetry

## Install dependencies using poetry
RUN poetry config virtualenvs.create false && \
    poetry install --no-dev

# Run main.py when the container launches
CMD ["python", "main.py"]