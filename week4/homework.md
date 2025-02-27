# Module 3 Homework: Data Warehouse

Homework instructions for week4: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/04-analytics-engineering/homework.md)

---

### Question 1

After setting up `sources.yml` and the environment variables, compile the `.sql` model outputs:

```sql
SELECT *
FROM myproject.raw_nyc_tripdata.ext_green_taxi
```

### Question 2

For command line arguments to take precedence over ENV_VARs, we need var on the outside and then env_var on the inside. So, it would be

```sql
Update the WHERE clause to pickup_datetime >= CURRENT_DATE - INTERVAL '{{ var("days_back", env_var("DAYS_BACK", "30")) }}' DAY.
```

### Question 3

```sql
dbt run --select models/staging/+
```

### Question 4

- Setting a value for DBT_BIGQUERY_TARGET_DATASET env var is mandatory, or it'll fail to compile (True)

- Setting a value for DBT_BIGQUERY_STAGING_DATASET env var is mandatory, or it'll fail to compile (False)

- When using core, it materializes in the dataset defined in DBT_BIGQUERY_TARGET_DATASET (True)

- When using stg, it materializes in the dataset defined in DBT_BIGQUERY_STAGING_DATASET, or defaults to DBT_BIGQUERY_TARGET_DATASET (True)

- When using staging, it materializes in the dataset defined in DBT_BIGQUERY_STAGING_DATASET, or defaults to DBT_BIGQUERY_TARGET_DATASET(True).
