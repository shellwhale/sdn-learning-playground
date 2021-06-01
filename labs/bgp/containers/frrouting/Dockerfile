FROM debian:buster

ENV DEBIAN_FRONTEND noninteractive
ENV APT_KEY_DONT_WARN_ON_DANGEROUS_USAGE=DontWarn
RUN apt-get update && apt-get install -y \
    traceroute \
    net-tools \
    iputils-ping \
    iproute2 \
    telnet telnetd \
    iperf \
    iperf3 \
    net-tools \
    iputils-ping \
    iproute2 \
    libpcre3-dev \
    apt-transport-https \
    ca-certificates \
    curl \
    wget \
    logrotate \
    libc-ares2 \
    libjson-c3 \
    procps \
    libreadline7 \
    gnupg2 \
    lsb-release \
    apt-utils \
    tcpdump

RUN curl -s https://deb.frrouting.org/frr/keys.asc | apt-key add -
RUN echo deb https://deb.frrouting.org/frr $(lsb_release -s -c) frr-stable | tee -a /etc/apt/sources.list.d/frr.list

RUN apt-get update && apt-get install -y \
    frr \
    frr-pythontools

RUN chown -R frr:frr /etc/frr

COPY daemons /etc/frr/daemons
COPY frr.conf /etc/frr/frr.conf

ENTRYPOINT /etc/init.d/frr start
