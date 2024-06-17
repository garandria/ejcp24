FROM debian:latest

RUN apt-get update && apt-get install -y locales && rm -rf /var/lib/apt/lists/* \
	&& localedef -i en_US -c -f UTF-8 -A /usr/share/locale/locale.alias en_US.UTF-8
ENV LANG en_US.utf8

RUN <<EOF
    apt-get update && apt-get install -y default-jre default-jdk python3 python3-pip python3-venv wget git
    wget https://github.com/joular/powerjoular/releases/download/0.7.3/powerjoular_0.7.3_amd64.deb
    dpkg -i powerjoular_0.7.3_amd64.deb
EOF
