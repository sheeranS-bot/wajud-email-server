# Use Python base image
FROM python:3.9

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Install dependencies
RUN pip install -r requirements.txt

# Expose port
EXPOSE 8080

# Run Flask app
CMD ["python", "email_server.py"]