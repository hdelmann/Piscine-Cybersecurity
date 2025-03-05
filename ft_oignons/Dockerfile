FROM debian:latest

RUN apt-get update && apt-get install -y \
    nginx \
    tor \
    openssh-server \
    curl \
    && rm -rf /var/lib/apt/lists/*

RUN mkdir /var/run/sshd
RUN chown -R www-data:www-data /var/www/html /var/log/nginx

COPY nginx.conf /etc/nginx/nginx.conf
COPY index.html /var/www/html/index.html
COPY sshd_config /etc/ssh/sshd_config
COPY torrc /etc/tor/torrc

COPY entrypoint.sh /entrypoint.sh

RUN chmod +x /entrypoint.sh

EXPOSE 80 4242

RUN mkdir -p /var/lib/tor/hidden_service && \
    chown -R debian-tor:debian-tor /var/lib/tor/hidden_service && \
    chmod 700 /var/lib/tor/hidden_service



CMD ["/entrypoint.sh"]