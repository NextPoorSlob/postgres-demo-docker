# Postgres Docker
A simple Postgres SQL database running in a Docker container. The run creates a persistent volume for the data, so the
database is stable from one run to the next.

## Generate Data
Before running Docker and starting up the database, you will need data files. Use the generate-demo-data.py script in the
data-generator directory.

```text
python generate-demo-data.py -h

usage: generate-demo-data.py [-h] [-c CUSTOMERS] [-p PRODUCTS] [-o ORDERS]

options:
  -h, --help            show this help message and exit
  -c CUSTOMERS, --customers CUSTOMERS
                        Number of customers to generate. Default is 2000
  -p PRODUCTS, --products PRODUCTS
                        Number of products to generate. Default is 10000
  -o ORDERS, --orders ORDERS
                        Number of orders to generate. Default is 20000000
```

If you just run with the defaults, you will have 20,000,000 records in the orders table. If that is too big, you can use
the overrides to make thing smaller. Or larger.

When the Docker container starts up for the first time, it will create the tables using the generated data. To refresh
the data, simply delete the volume (see below).

## Running Docker
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
