FROM python:3.13-slim

ENV POETRY_VIRTUALENVS_CREATE=false

ARG USER_NAME=user
ARG GROUP_NAME=user_group
ARG UID=1234
ARG GID=4321

# Create user and group with specified UID and GID
RUN groupadd -g ${GID} ${GROUP_NAME} && \
    useradd -u ${UID} -g ${GROUP_NAME} -s /sbin/nologin -m -d /home/${USER_NAME} ${USER_NAME}

# Install Poetry via pip
RUN pip install poetry

WORKDIR /app

# Copy and install dependencies as root
COPY pyproject.toml poetry.lock ./
RUN poetry install --no-root --no-interaction --without dev

# Adjust permissions and switch to the created user
RUN chown -R ${USER_NAME}:${GROUP_NAME} /app
USER ${USER_NAME}

# Copy the rest of the application code
COPY --chown=${USER_NAME}:${GROUP_NAME} . .

EXPOSE 8000

RUN chmod +x entrypoint.sh

CMD ["poetry", "run", "uvicorn", "playground_api.app:app", "--host", "0.0.0.0", "--port", "8000"]
