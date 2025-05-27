# Postgres Docker
A simple Postgres SQL database running in a Docker container. The run creates a persistent volume for the data, so the
database is stable from one run to the next.

To run:
```text
docker-compose up -d
```

To stop:
```text
docker-compose down
```

To clear the database:
```text
docker volume rm postgres-demo-docker_postgres-data
```

The `.env` file contains the environmental variable values for the run.

## Running pgAdmin4 In The Container
The latest version of pgAdmin4 will start up automatically with the Postgres SQL server. To sign on, go to:
http://localhost:3100 (The port will be different if you have changed the PGADMIN_EXPOSED_PORT value).

The default sign on credentials are:
* Username: pgadmin@pgadmin.com
* Password: pgadmin


The Postgres server is already registered, the the first time you use it, you will need to set the password, which is
`postgres`.
If you change port or credentials in the .env file, then use those.
* Hostname/address: **database** (use **localhost** if connecting with Datagrip or DBeaver)
* port: **5432**
* Username: **postgres**
* Password: **postgres**

To clear the admin data:
```text
docker volume rm postgres-demo-docker_pgadmin-data
```

The pgadmin-data volume and the pgadmin service can be removed if not needed.

## Opening SQL Files In pgAdmin4 A Container
pgAdmin4 does not have access to your host file system. To run a script in the Query Tool, do not try to open the script.
Instead, find the script in your file manager and drag the file into the Query Tool.

However, the scripts used in the presentation are preloaded to the pgAdmin4 file system, so they are available to open.
