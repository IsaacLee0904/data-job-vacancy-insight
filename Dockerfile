FROM python:3.11-slim

# Set the working directory to /app inside the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install system packages including git and Chrome dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    libatlas-base-dev \
    tzdata \
    git \
    libpq-dev \
    wget \
    gnupg \
    unzip \
    curl \
    xvfb \
    && rm -rf /var/lib/apt/lists/*

# Install Chrome
RUN wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add - \
    && echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list \
    && apt-get update \
    && apt-get install -y google-chrome-stable \
    && rm -rf /var/lib/apt/lists/*

# Set the time zone
RUN ln -fs /usr/share/zoneinfo/Asia/Taipei /etc/localtime && dpkg-reconfigure -f noninteractive tzdata

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Make port 80 available to the world outside this container
EXPOSE 80

# Define an environment variable
ENV NAME=JobVacancyInsight

CMD ["/bin/bash", "-c", "source activate env && python main.py"]
