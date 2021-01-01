FROM ubuntu:20.04

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update && apt-get install -y --install-recommends \
    bash git build-essential cmake time python3 python3-setuptools python3-pip python3-venv nginx && \
    apt-get clean && rm -rf /var/lib/apt/lists/* /tmp/* /var/tmp/* && \
    python3 -m venv /opt/venv/ && . /opt/venv/bin/activate && \
    pip install -U wheel setuptools pip && \
    rm -r ~/.cache/pip && rm -f "/etc/nginx/sites-enabled/default" && mkdir -p "/var/www/html/gwc"

COPY . /opt/gwc-hacking
ENV VIRTUAL_ENV "/opt/venv"
ENV PYTHONPATH "/opt/gwc-hacking:"
ENV PATH "/opt/venv/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin"
RUN pip install -r /opt/gwc-hacking/requirements.txt && \
    rm -r ~/.cache/pip && \
    ln -sf "/opt/gwc-hacking/static" "/var/www/html/gwc/static" && \
    ln -sf "/opt/gwc-hacking/config/nginx.site" "/etc/nginx/sites-enabled/gwc"
WORKDIR "/opt/gwc-hacking"
ENTRYPOINT ["/opt/gwc-hacking/run.sh"]