FROM python:3.8-slim-buster

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any necessary packages specified in requirements.txt
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an environment variable
ENV NAME JobVacancyInsight

# Run app.py when the container launches
# CMD ["python", "main.py"]