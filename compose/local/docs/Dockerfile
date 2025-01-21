# Use a lightweight Python base image
FROM python:3.12.8-alpine AS python

# Python base stage
ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

# Install dependencies
RUN apk update && apk add --no-cache \
    # Runtime dependencies
    make \
    gettext \
    && rm -rf /var/cache/apk/*

# Install MkDocs and required plugins
RUN pip install mkdocs==1.5.1 mkdocs-material==9.1.15 mkdocs-markdownextradata-plugin

# Copy the start script
COPY ./compose/local/docs/start /start-docs
RUN sed -i 's/\r$//g' /start-docs
RUN chmod +x /start-docs

WORKDIR /docs
