FROM oraclelinux:9-slim AS installer

ARG HELM_VERSION="v3.15.4"
ARG HELMFILE_VERSION="0.168.0"
ARG SOPS_VERSION="v3.9.0"
ARG HELM_PLUGIN_SECRETS_VERSION="v4.6.1"
ARG HELM_PLUGIN_DIFF_VERSION="v3.9.10"

ENV HELM_FILENAME="helm-${HELM_VERSION}-linux-amd64.tar.gz"
ENV HELMFILE_FILENAME="helmfile_${HELMFILE_VERSION}_linux_amd64.tar.gz"
ENV HELM_DATA_HOME=/usr/local/share/helm

RUN microdnf update \
    && microdnf --setopt=tsflags=nodocs \
    -y install tar gzip git jq

RUN curl -L https://github.com/helmfile/helmfile/releases/download/v${HELMFILE_VERSION}/helmfile_${HELMFILE_VERSION}_linux_amd64.tar.gz \
    -o /tmp/${HELMFILE_FILENAME} \
    && tar -zxvf /tmp/${HELMFILE_FILENAME} -C /tmp \
    && mv /tmp/helmfile /usr/local/bin/helmfile \
    && curl -L https://github.com/getsops/sops/releases/download/${SOPS_VERSION}/sops-${SOPS_VERSION}.linux.amd64 -o /usr/local/bin/sops \
    && curl -L https://get.helm.sh/${HELM_FILENAME} -o /tmp/${HELM_FILENAME} \
    && tar -zxvf /tmp/${HELM_FILENAME} -C /tmp \
    && mv /tmp/linux-amd64/helm /usr/local/bin/helm

RUN chmod +x /usr/local/bin/helmfile /usr/local/bin/helm /usr/local/bin/sops

RUN  helm plugin install https://github.com/jkroepke/helm-secrets --version ${HELM_PLUGIN_SECRETS_VERSION} \
    && helm plugin install https://github.com/databus23/helm-diff --version ${HELM_PLUGIN_DIFF_VERSION}
RUN microdnf clean all && rm -rf /tmp/*

FROM python:3.12-slim AS builder
RUN pip install --user pipenv==2024.0.1
ENV PIPENV_VENV_IN_PROJECT=1
COPY Pipfile* /usr/src/
WORKDIR /usr/src

### Comment out all instructions below to update Pipfile.lock
### And run the command:
### docker build -t deploy-backend-build deploy_backend && docker run --rm -ti -v $(pwd)/deploy_backend:/usr/src deploy-backend-build bash
### Then inside the shell run: python -m pipenv lock

RUN python -m pipenv sync

FROM python:3.12-slim AS production
ENV PYTHONUNBUFFERED=1
ENV WORKDIR=/app
ENV PYTHONPATH=${WORKDIR}
ENV HELM_DATA_HOME=/usr/local/share/helm
WORKDIR ${WORKDIR}
# Upgrade for security reasons
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/src/.venv /.venv
COPY --from=installer /usr/local/bin/helm /usr/local/bin/helm
COPY --from=installer /usr/local/bin/helmfile /usr/local/bin/helmfile
COPY --from=installer /usr/local/bin/sops /usr/local/bin/sops
COPY --from=installer /usr/local/share/helm/plugins /usr/local/share/helm/plugins
COPY src .

CMD ["/.venv/bin/python", "-m", "main"]