FROM python:3.10

# install firefox
RUN apt-get update                             \
 && apt-get install -y --no-install-recommends \
    ca-certificates curl firefox-esr           \
 && rm -fr /var/lib/apt/lists/*                \
 && curl -L https://github.com/mozilla/geckodriver/releases/download/v0.30.0/geckodriver-v0.30.0-linux64.tar.gz | tar xz -C /usr/local/bin \
 && apt-get purge -y ca-certificates curl

# set display port to avoid crash
ENV DISPLAY=:99

COPY requirements.txt ./requirements.txt
RUN pip install --default-timeout=100 -r requirements.txt

COPY . app/
WORKDIR app

ARG ACCESS_KEY_ID
ARG SECRET_ACCESS_KEY
ENV ACCESS_KEY_ID ${ACCESS_KEY_ID}
ENV SECRET_ACCESS_KEY ${SECRET_ACCESS_KEY}

CMD scrapy crawl tweet_scraper