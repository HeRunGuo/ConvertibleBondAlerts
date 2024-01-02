# Use an official Python runtime as a parent image
FROM python:3.8-slim

# Set the working directory in the container
WORKDIR /usr/src/app

# Copy the current directory contents into the container at /usr/src/app
COPY . .

# Set the timezone environment variable
ENV TZ=Asia/Shanghai
ENV BARK_TOKEN=your_bark_token_here

# Install tzdata, cron, and any needed packages specified in requirements.txt
RUN apt-get update \
    && apt-get install -y --no-install-recommends tzdata cron \
    && ln -snf /usr/share/zoneinfo/$TZ /etc/localtime && echo $TZ > /etc/timezone \
    && pip install --no-cache-dir -r requirements.txt \
    && RUN python3 --version


# Add crontab file in the cron directory
ADD crontab /etc/cron.d/my-cron-job

# Give execution rights on the cron job
RUN chmod 0644 /etc/cron.d/my-cron-job

# Apply cron job
RUN crontab /etc/cron.d/my-cron-job

# Run the command on container startup
CMD cron && tail -f /var/log/cron.log
