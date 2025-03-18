FROM ubuntu:24.04

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

# Install pip
RUN apt-get update && apt-get install -y \
    python3-pip

# Install chromedriver
RUN wget https://chromedriver.storage.googleapis.com/114.0.5735.90/chromedriver_linux64.zip \
&& unzip chromedriver_linux64.zip \
&& mv chromedriver /usr/bin/chromedriver \
&& chmod +x /usr/bin/chromedriver \
&& rm chromedriver_linux64.zip

RUN pip install --no-cache-dir -r requirements.txt

# ENV PATH="/app:${PATH}"

CMD [ "python", "./api.py" ]
