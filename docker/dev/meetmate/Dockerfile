FROM python:3.10.4

WORKDIR /apps/meetmate
COPY ./apps/meetmate/requirements /apps/meetmate/requirements
RUN pip3 install -r /apps/meetmate/requirements/base.txt

COPY ./apps/meetmate /apps/meetmate


RUN curl -fsSL https://deb.nodesource.com/setup_current.x | bash -
RUN apt-get install -y nodejs
RUN echo "deb http://deb.debian.org/debian sid main" >> /etc/apt/sources.list
#RUN curl http://dl.google.com/linux/chrome/deb/pool/main/g/google-chrome-stable/google-chrome-stable_93.0.4577.82-1_amd64.deb --output /chromium.deb
#RUN dpkg -i  /chromium.deb
#RUN apt install -y -f chromium=90.0.4430.212-1
RUN #apt update
#RUN apt install -y wkhtmltopdf
#RUN chmod 777 /usr/bin/wkhtmltopdf


COPY ./docker/dev/meetmate/entrypoint.sh /
RUN chmod +x /entrypoint.sh

#ENTRYPOINT ["chromium", "--no-sandbox", "--disable-dev-shm-usage", "--disable-gpu"]
ENTRYPOINT [ "/entrypoint.sh" ]
