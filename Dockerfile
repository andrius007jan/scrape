FROM python:3.11-alpine

EXPOSE 8000

WORKDIR /app

COPY requirements.txt .
COPY src/scraping_service /app/scraping_service
COPY startup.sh .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Install temporary dependencies
RUN apk update && apk upgrade && \
    apk add --no-cache --virtual .build-deps \
    alpine-sdk \
    curl \
    wget \
    unzip \
    gnupg

# Install dependencies
RUN apk add --no-cache \
    xvfb \
    x11vnc \
    fluxbox \
    xterm \
    libffi-dev \
    openssl-dev \
    zlib-dev \
    bzip2-dev \
    readline-dev \
    sqlite-dev \
    git \
    nss \
    freetype \
    freetype-dev \
    harfbuzz \
    ca-certificates \
    ttf-freefont \
    chromium
# Install x11vnc
RUN mkdir ~/.vnc
RUN x11vnc -storepasswd 1234 ~/.vnc/passwd

ENV PATH="/scripts:$PATH"
ENV DISPLAY=:0

# Delete temporary dependencies
RUN apk del .build-deps

CMD ["sh", "startup.sh"]