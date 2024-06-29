# Use Python 3.12.4 as the base image
FROM python:3.12.4-slim

# Set the working directory in the container
WORKDIR /bot

# Copy the current directory contents into the container at /bot
COPY . /bot

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Run the bot, printing any output to the container's logs
CMD ["python", "main.py"]