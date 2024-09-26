# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install build-essential to get gcc and other tools
RUN apt-get update && apt-get install -y build-essential

# Set the working directory
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app/

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables (optional)
ENV PYTHONUNBUFFERED=1

# Expose port 8000
EXPOSE 8000

# Command to run the Django development server
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
