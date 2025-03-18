FROM python:3

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y \
    libgconf-2-4 \
    libatk1.0-0 \
    libatk-bridge2.0-0 \
    libcups2 \
    libdrm2 \
    libxkbcommon0 \
    libxcomposite1 \
    libxdamage1 \
    libxfixes3 \
    libxrandr2 \
    libgbm1 \
    fonts-liberation \
    xdg-utils \
    wget \
    unzip

RUN chmod +x ./chromedriver

ENV PATH="/app:${PATH}"

CMD [ "python", "./api.py" ]
