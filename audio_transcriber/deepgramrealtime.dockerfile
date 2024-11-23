# Use an official Python image as the base
FROM python:3.10-slim

# Set the working directory inside the container
WORKDIR /app

# Ensure repositories are updated and fix any missing packages
RUN apt-get update && apt-get upgrade -y && apt-get install -y \
    build-essential \
    portaudio19-dev \
    libportaudio2 \
    libportaudiocpp0 \
    ffmpeg \
    --fix-missing \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements.txt to the working directory
COPY requirements.txt .

# Install Python dependencies
RUN pip install -r requirements.txt

# Copy the script and other necessary files to the working directory
COPY . .

# Set the command to run the script
CMD ["python", "realtime_transcribe.py"]
