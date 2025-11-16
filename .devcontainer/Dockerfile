# Base image for Codespaces
FROM mcr.microsoft.com/vscode/devcontainers/base:ubuntu

USER root

###############################
# Install core tools
###############################
RUN apt-get update && \
    apt-get install -y \
      docker.io \
      docker-compose \
      curl \
      wget \
      unzip \
      ca-certificates \
      gnupg \
      lsb-release \
      python3 \
      python3-pip \
      git \
      vim && \
    apt-get clean

###############################
# Install Terraform
###############################
RUN wget -O- https://apt.releases.hashicorp.com/gpg | \
    gpg --dearmor -o /usr/share/keyrings/hashicorp-archive-keyring.gpg && \
    echo "deb [signed-by=/usr/share/keyrings/hashicorp-archive-keyring.gpg] \
    https://apt.releases.hashicorp.com $(lsb_release -cs) main" \
    > /etc/apt/sources.list.d/hashicorp.list && \
    apt-get update && \
    apt-get install -y terraform

###############################
# Install Trivy
###############################
RUN wget https://github.com/aquasecurity/trivy/releases/latest/download/trivy_0.50.1_Linux-64bit.deb && \
    dpkg -i trivy_0.50.1_Linux-64bit.deb && \
    rm trivy_0.50.1_Linux-64bit.deb

###############################
# Install Hadolint
###############################
RUN wget -O /usr/local/bin/hadolint \
    https://github.com/hadolint/hadolint/releases/download/v2.12.0/hadolint-Linux-x86_64 && \
    chmod +x /usr/local/bin/hadolint

###############################
# Install Conftest (OPA)
###############################
RUN wget https://github.com/open-policy-agent/conftest/releases/latest/download/conftest_0.52.0_Linux_x86_64.tar.gz \
    && tar -xzf conftest_0.52.0_Linux_x86_64.tar.gz \
    && mv conftest /usr/local/bin \
    && chmod +x /usr/local/bin/conftest \
    && rm conftest_0.52.0_Linux_x86_64.tar.gz

###############################
# Setup Python Tools
###############################
RUN pip3 install -U pip && \
    pip3 install pytest

###############################
# Optional: Docker-in-Docker Permissions
###############################
RUN usermod -aG docker vscode || true

###############################
# Workspace Setup
###############################
WORKDIR /workspace

# Post-creation script to finalize setup
RUN echo '#!/bin/bash\npip3 install -U pip\n' > /usr/local/bin/setup-tools.sh && \
    chmod +x /usr/local/bin/setup-tools.sh

