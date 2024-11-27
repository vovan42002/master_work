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
WORKDIR ${WORKDIR}
# Upgrade for security reasons
RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get autoremove -y \
    && apt-get clean -y \
    && rm -rf /var/lib/apt/lists/*
COPY --from=builder /usr/src/.venv /.venv
COPY src .

CMD ["/.venv/bin/python", "-m", "main"]