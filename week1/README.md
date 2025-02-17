## Docker and SQL

Instructions for week1: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/README.md)

## Commands

All the commands from the video

Downloading the data in parquet or csv file

```bash
wget https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet
wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz
```

### Running Postgres with Docker

#### Windows

Running Postgres on Windows (note the full path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/pc/Documents/Github/data-engineering-zoomcamp/week1/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  postgres:13
```

### CLI for Postgres

Installing `pgcli`

```bash
pip install pgcli
```

Using `pgcli` to connect to Postgres

```bash
pgcli -h localhost -p 5432 -u root -d ny_taxi
```

### NY Trips Dataset

Dataset:

- https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- https://www1.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

> According to the [TLC data website](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page),
> from 05/13/2022, the data will be in `.parquet` format instead of `.csv`
> The website has provided a useful [link](https://www1.nyc.gov/assets/tlc/downloads/pdf/working_parquet_format.pdf) with sample steps to read `.parquet` file and convert it to Pandas data frame.
>
> You can use the csv backup located here, https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz, to follow along with the video.

```
$ aws s3 ls s3://nyc-tlc
                           PRE csv_backup/
                           PRE misc/
                           PRE trip data/
```

You can refer the `data-loading-parquet.ipynb` and `data-loading-parquet.py` for code to handle both csv and paraquet files. (The lookup zones table which is needed later in this course is a csv file)

> Note: You will need to install the `pyarrow` library. (add it to your Dockerfile)

### pgAdmin

Running pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  dpage/pgadmin4
```

### Running Postgres and pgAdmin together

Create a network

```bash
docker network create pg-network
```

Run Postgres (change the path)

```bash
docker run -it \
  -e POSTGRES_USER="root" \
  -e POSTGRES_PASSWORD="root" \
  -e POSTGRES_DB="ny_taxi" \
  -v c:/Users/pc/Documents/Github/data-engineering-zoomcamp/week1/ny_taxi_postgres_data:/var/lib/postgresql/data \
  -p 5432:5432 \
  --network=pg-network \
  --name pg-database \
  postgres:13
```

Run pgAdmin

```bash
docker run -it \
  -e PGADMIN_DEFAULT_EMAIL="admin@admin.com" \
  -e PGADMIN_DEFAULT_PASSWORD="root" \
  -p 8080:80 \
  --network=pg-network \
  --name pgadmin-2 \
  dpage/pgadmin4
```

### Data ingestion

Running locally

```bash
URL="https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2023-09.parquet"

python ingest_data.py \
  --user=root \
  --password=root \
  --host=localhost \
  --port=5432 \
  --db=ny_taxi \
  --tb=yellow_taxi_trips \
  --url=${URL}
```

Build the image

```bash
docker build -t taxi_ingest:v001 .
```

Run the script with Docker

```bash
URL="https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/yellow_tripdata_2021-01.csv.gz"

docker run -it \
  --network=pg-network \
  taxi_ingest:v001 \
    --user=root \
    --password=root \
    --host=pg-database \
    --port=5432 \
    --db=ny_taxi \
    --tb=yellow_taxi_trips \
    --url=${URL}
```

### Docker-Compose

Run it:

```bash
docker-compose up
```

Run in detached mode:

```bash
docker-compose up -d
```

Shutting it down:

```bash
docker-compose down
```

Note: to make pgAdmin configuration persistent, create a folder `data_pgadmin` and mount it to the `/var/lib/pgadmin` folder:

```yaml
services:
  pgadmin:
    image: dpage/pgadmin4
    volumes:
      - ./data_pgadmin:/var/lib/pgadmin
    ...
```

### SQL Refresher

Pre-Requisites: If you followed the course through with the given order,
Docker Compose should be already running with pgdatabase and pgAdmin.

You can run the following code using Jupyter Notebook to ingest the data for Taxi Zones:

```python
import pandas as pd
from sqlalchemy import create_engine

engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')
engine.connect()

!wget https://github.com/DataTalksClub/nyc-tlc-data/releases/download/misc/taxi_zone_lookup.csv

df_zones = pd.read_csv("taxi_zone_lookup.csv")
df_zones.to_sql(name='zones', con=engine, if_exists='replace')
```

Once done, you can go to http://localhost:8080/browser/ to access pgAdmin.
Don't forget to Right Click on the server or database to refresh it in case you don't see the new table.

Now start querying!

Joining Yellow Taxi table with Zones Lookup table (implicit INNER JOIN)

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM
    yellow_taxi_trips t,
    zones zpu,
    zones zdo
WHERE
    t."PULocationID" = zpu."LocationID"
    AND t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

Joining Yellow Taxi table with Zones Lookup table (Explicit INNER JOIN)

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM
    yellow_taxi_trips t
JOIN
-- or INNER JOIN but it's less used, when writing JOIN postgreSQL undranstands implicitly that we want to use an INNER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

Checking for records with NULL Location IDs in the Yellow Taxi table

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips t
WHERE
    "PULocationID" IS NULL
    OR "DOLocationID" IS NULL
LIMIT 100;
```

Checking for Location IDs in the Zones table NOT IN the Yellow Taxi table

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    "PULocationID",
    "DOLocationID"
FROM
    yellow_taxi_trips t
WHERE
    "DOLocationID" NOT IN (SELECT "LocationID" from zones)
    OR "PULocationID" NOT IN (SELECT "LocationID" from zones)
LIMIT 100;
```

Using LEFT, RIGHT, and OUTER JOINS when some Location IDs are not in either Tables

```sql
DELETE FROM zones WHERE "LocationID" = 142;

SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM
    yellow_taxi_trips t
LEFT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM
    yellow_taxi_trips t
RIGHT JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

```sql
SELECT
    tpep_pickup_datetime,
    tpep_dropoff_datetime,
    total_amount,
    CONCAT(zpu."Borough", ' | ', zpu."Zone") AS "pickup_loc",
    CONCAT(zdo."Borough", ' | ', zdo."Zone") AS "dropff_loc"
FROM
    yellow_taxi_trips t
OUTER JOIN
    zones zpu ON t."PULocationID" = zpu."LocationID"
JOIN
    zones zdo ON t."DOLocationID" = zdo."LocationID"
LIMIT 100;
```

Using GROUP BY to calculate number of trips per day

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
LIMIT 100;
```

Using ORDER BY to order the results of your query

```sql
-- Ordering by day

SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1)
FROM
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "day" ASC
LIMIT 100;

-- Ordering by count

SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count"
FROM
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

Other kinds of aggregations

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM
    yellow_taxi_trips t
GROUP BY
    CAST(tpep_dropoff_datetime AS DATE)
ORDER BY
    "count" DESC
LIMIT 100;
```

Grouping by multiple fields

```sql
SELECT
    CAST(tpep_dropoff_datetime AS DATE) AS "day",
    "DOLocationID",
    COUNT(1) AS "count",
    MAX(total_amount) AS "total_amount",
    MAX(passenger_count) AS "passenger_count"
FROM
    yellow_taxi_trips t
GROUP BY
    1, 2
ORDER BY
    "day" ASC,
    "DOLocationID" ASC
LIMIT 100;
```

## Local Setup for Terraform and GCP

### Pre-Requisites
- Terraform client installation: [Download Terraform](https://www.terraform.io/downloads)
- Cloud Provider account: [Google Cloud Console](https://console.cloud.google.com/)

### Terraform Concepts
[Terraform Overview](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/1_terraform_overview.md)

### GCP Setup
1. [Setup for First-time](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#initial-setup)
   - [Only for Windows](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/windows.md) - Steps 4 & 5
2. [IAM / Access specific to this course](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/01-docker-terraform/1_terraform_gcp/2_gcp_overview.md#setup-for-access)

## Terraform Workshop for GCP Infra
Your setup is ready! Now head to the [terraform](https://github.com/DataTalksClub/data-engineering-zoomcamp/tree/main/01-docker-terraform/1_terraform_gcp/terraform) directory, and perform the execution steps to create your infrastructure.
