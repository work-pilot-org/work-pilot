FROM prom/prometheus:v2.51.0

ARG CAE_DOMAIN=internal
USER root
RUN mkdir -p /etc/prometheus
COPY ./monitoring/prometheus/prometheus.yml /etc/prometheus/prometheus.yml.template

# Replace service targets at build or container start
RUN sed -e "s/auth-service:8000/auth-service.${CAE_DOMAIN}:80/g" \
        -e "s/hr-service:8000/hr-service.${CAE_DOMAIN}:80/g" \
        -e "s/it-service:8000/it-service.${CAE_DOMAIN}:80/g" \
        -e "s/workflow-service:8000/workflow-service.${CAE_DOMAIN}:80/g" \
        -e "s/notification-service:8000/notification-service.${CAE_DOMAIN}:80/g" \
        -e "s/analytics-service:8000/analytics-service.${CAE_DOMAIN}:80/g" \
        -e "s/ai-service:8000/ai-service.${CAE_DOMAIN}:80/g" \
        /etc/prometheus/prometheus.yml.template > /etc/prometheus/prometheus.yml

USER nobody
EXPOSE 9090
ENTRYPOINT [ "/bin/prometheus" ]
CMD [ "--config.file=/etc/prometheus/prometheus.yml", \
      "--storage.tsdb.path=/prometheus", \
      "--web.console.libraries=/usr/share/prometheus/console_libraries", \
      "--web.console.templates=/usr/share/prometheus/consoles" ]
