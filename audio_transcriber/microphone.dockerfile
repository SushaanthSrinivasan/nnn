# Use the official Python 3.10 slim image
FROM python:3.10-slim

# Install system dependencies for audio recording and MP3 conversion
RUN apt-get update && apt-get install -y \
    ffmpeg \
    libportaudio2 \
    && rm -rf /var/lib/apt/lists/*

# Set the working directory in the container
WORKDIR /app

# Copy the Python script into the container
COPY recorder.py /app/

# Install required Python libraries
RUN pip install --no-cache-dir sounddevice pydub scipy numpy

# Entry point for the container to run the recorder script
ENTRYPOINT ["python", "recorder.py"]
