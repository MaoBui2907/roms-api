# Use a lightweight Linux distribution and python 3.10
FROM python:3.10.13-alpine3.19

# Install cron and other required packages
RUN apk add --update apk-cron && rm -rf /var/cache/apk/*

# Copy your application files to the container
COPY roms/ /app

# Set the working directory
WORKDIR /app

# Install the required Python packages
RUN pip3 install --upgrade pip

# Install the required Python packages
RUN pip3 install pipenv
RUN pipenv install --skip-lock scrapy azure-cosmos toml

RUN ls -la /app

# Add your crontab file
COPY /roms/crontab /etc/crontabs/root

# Give execution rights on the cron job
RUN chmod 0644 /etc/crontabs/root

# Debugging
RUN ls -la /app
RUN ls -la /etc/crontabs/root
RUN date

# Start cron service when the container starts
CMD ["crond", "-f"]
