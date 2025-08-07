# Dockerfile
ARG VARIANT=3.10-bullseye
FROM mcr.microsoft.com/devcontainers/python:${VARIANT}

# Install system dependencies as root
# git is already in the base image, so we only need to add make
RUN apt-get update && export DEBIAN_FRONTEND=noninteractive \
    && apt-get -y install --no-install-recommends make

# --- Python Environment Setup ---

# Define a path for the virtual environment
ENV VENV_PATH=/opt/venv
# Add the venv's bin directory to the PATH.
# This makes the venv's python/pip the default for all terminals.
ENV PATH="${VENV_PATH}/bin:${PATH}"

# Create the virtual environment and give the vscode user ownership
RUN python3 -m venv ${VENV_PATH} && \
    chown -R vscode:vscode ${VENV_PATH}

# Copy requirements.txt first to leverage Docker cache
# If requirements.txt doesn't change, this layer won't be rebuilt
COPY requirements.txt .

# Switch to the non-root user to install packages
USER vscode

# Install Python packages into the virtual environment
RUN pip install --no-cache-dir -r requirements.txt

# Set the working directory
WORKDIR /workspace