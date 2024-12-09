FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Create package directory
RUN mkdir compute_pkg

# Copy the application files
COPY compute.py compute_pkg/compute.py
RUN ln -s compute_pkg/compute.py compute
COPY test_compute.py .

# Make compute.py executable
RUN chmod +x compute

# Create empty __init__.py to make directory a Python package
RUN touch compute_pkg/__init__.py

# Default to compute mode
ENTRYPOINT ["./compute"]

# Allow overriding entrypoint for test mode
# Usage: docker run --entrypoint pytest solution -v test_compute.py