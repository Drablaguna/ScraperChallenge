FROM python:3.11-bookworm

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

COPY . /app

# Install requests dependencies
RUN apt-get update && apt-get install -y \
wget \
gnupg \
lsb-release \
unzip

# Add chrome repo
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb \
&& apt-get install ./google-chrome-stable_current_amd64.deb -y \
&& rm google-chrome-stable_current_amd64.deb

# Install chromedriver
RUN wget https://storage.googleapis.com/chrome-for-testing-public/134.0.6998.88/linux64/chromedriver-linux64.zip \
&& unzip chromedriver-linux64.zip \
&& mv ./chromedriver-linux64/chromedriver /usr/bin/chromedriver \
&& chmod +x /usr/bin/chromedriver \
&& rm chromedriver-linux64.zip

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./api.py" ]
