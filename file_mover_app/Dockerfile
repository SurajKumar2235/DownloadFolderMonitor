# Use a Python base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the Python script and .env file into the container
COPY script.py .
COPY .env .

# Install dependencies
RUN pip install watchdog plyer python-dotenv

# Create directories if they don't exist
RUN mkdir -p /home/user/Downloads /home/user/Documents

# Start the file mover script when the container starts
CMD ["python", "script.py"]
