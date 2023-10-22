FROM redis:7.0.0

RUN mkdir -p /etc/redis/
RUN echo "requirepass redis" > /etc/redis/redis.conf

CMD ["redis-server", "/etc/redis/redis.conf"]