FROM python:3.11-slim

# Update
RUN apt-get update && \
    apt-get install -y ffmpeg curl unzip

# Install dependencies
COPY ./requirements.txt /app/requirements.txt
WORKDIR /app
RUN pip install -r requirements.txt && \
    playwright install && \
    playwright install-deps

# Add scripts
COPY . /app

# Set default command
CMD ["python", "-u", "src/main.py"]
