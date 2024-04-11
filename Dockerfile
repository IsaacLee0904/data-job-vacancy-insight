FROM python:3.8-slim-buster

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system packages including git
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    tzdata \
    git  # Add git here

# Set the time zone
RUN ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an environment variable
ENV NAME JobVacancyInsight

CMD ["/bin/bash", "-c", "source activate env && python main.py"]
