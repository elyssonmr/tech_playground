Installing
====

After downloading the repository. Create a virtualenv using the tool you like. Add [Poetry](https://python-poetry.org/docs/#installation) to it and the run:

```shell
poetry install
```

After installing the project, you can run it using docker compose:

```shell
docker compose up -d
```

Or:

```shell
docker-compose up -d
```

The required database migrations are executed while the application container is starting.

The application are going to be available in: [https://localhost:8000](https://localhost:8000).


**OBS:** All common commands are documented in `pyproject.toml` at the end of the file.


Populating the database
====

There is a script that can be run to populate the database with the data provided by `data.csv`. Before running the script, it is required to configure a `.env` file with the database config. If you didn't change any docker compose configuration, just copy the content below and pate in a new `.env` file in the root of the project:

```
DATABASE_URL="postgresql+psycopg://playground:playground_passwd@localhost:5432/playground"
```

After creating the file you can run the script by executing:

```shell
task populate_db
```

Or:

```shell
poetry run task populate_db
```


Additional Info
====

This project have a automated CI/CD which creates a Docker image of the application and run it's tests at every push in the main branch. The image can be accessed here: [https://hub.docker.com/r/elyssonmr/tech_playground](https://hub.docker.com/r/elyssonmr/tech_playground).

It also have a changelog that was automatically generated using a tool for that. Basically we add new files containing the content of the changelog and then run the commands to generate the changelog and create a tag of version. This command bumps the version in some files of the project, generates the changelog and then creates a git tag.

Some of the unit tests are in reality integration tests between the API and a database. This database is created at the beginning of every tests run and destroyed after all tests ran.

This project was deployed to a internal server using Ansible. The Ansible script was responsible for configuring the host and running the application using a docker compose. It was not automated in the CI/CD because the server is in my house. The URL of the deployment was provided for those who has interest in this project.
