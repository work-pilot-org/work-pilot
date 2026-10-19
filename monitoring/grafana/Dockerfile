FROM grafana/grafana:10.4.1

# Pre-populate datasources, provider and dashboards
COPY ./monitoring/grafana/provisioning /etc/grafana/provisioning
COPY ./monitoring/grafana/dashboards /var/lib/grafana/dashboards

ENV GF_SECURITY_ADMIN_USER=admin \
    GF_SECURITY_ADMIN_PASSWORD=admin \
    GF_USERS_ALLOW_SIGN_UP=false

EXPOSE 3000
