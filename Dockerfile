# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

RUN pip install --upgrade pip
RUN mkdir -p logs && chmod -R 777 logs
# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt


# Switch to root user
USER root

EXPOSE 8080

# Run app.py when the container launches
CMD ["python", "app.py"]
