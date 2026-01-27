FROM python:3.13-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1

RUN pip install poetry

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --without dev

FROM python:3.13-slim AS runtime

ARG USER_NAME=user
ARG GROUP_NAME=user_group
ARG UID=1234
ARG GID=4321
RUN groupadd -g ${GID} ${GROUP_NAME} && \
    useradd -u ${UID} -g ${GROUP_NAME} -s /sbin/nologin -m -d /home/${USER_NAME} ${USER_NAME}
WORKDIR /app
COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"
COPY --chown=${USER_NAME}:${GROUP_NAME} . .
RUN chmod +x entrypoint.sh
USER ${USER_NAME}
EXPOSE 8000

CMD ["./entrypoint.sh"]
