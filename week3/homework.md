# Module 3 Homework: Data Warehouse

Homework instructions for week3: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/03-data-warehouse/homework.md)  

## Important Note
For this homework, we will be using the **Yellow Taxi Trip Records** for **January 2024 - June 2024**, **NOT** the entire year of data. The Parquet files can be found on the New York City Taxi Data website:
[NYC Taxi Data - TLC Trip Record Data](https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page)
You will need to use the **PARQUET option** files when creating an **External Table**.

---

## GCP SETUP
- Create an **external table** using the **Yellow Taxi Trip Records**.
- Create a **(regular/materialized) table** in **BigQuery (BQ)** using the **Yellow Taxi Trip Records** (**do not partition or cluster this table**).

```sql
CREATE OR REPLACE EXTERNAL TABLE `zoomcamp-450016.zoomcamp.external_yellow_tripdata`
OPTIONS (
  format = 'CSV',
  uris = ['gs://zoomcamp-fr-kestra-bucket/yellow_tripdata_2024-0*.parquet']
);
```
```sql
CREATE OR REPLACE TABLE zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned AS
SELECT * FROM zoomcamp-450016.zoomcamp.external_yellow_tripdata;
```

---

### Question 1: Option 3 => 20,332,093
**What is the count of records for the 2024 Yellow Taxi Data?**

```sql
SELECT COUNT(*) FROM `zoomcamp-450016.zoomcamp.external_yellow_tripdata`;
```
`20,332,093`

### Question 2: Option 2 => 0 MB for the External Table and 155.12 MB for the Materialized Table
**Write a query to count the distinct number of PULocationIDs for the entire dataset on both tables. What is the estimated amount of data that will be read when this query is executed on the External Table and the Table?**

```sql
SELECT COUNT( DISTINCT PULocationID )
FROM `zoomcamp-450016.zoomcamp.external_yellow_tripdata`;

SELECT COUNT( DISTINCT PUlocationID )
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned`;
```
`0 MB for the External Table and 155.12 MB for the Materialized Table`

External tables are not stored in BigQuery, they point to files in Google Cloud Storage.

### Question 3: Option 1 => BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.
**Write a query to retrieve the PULocationID from the table (not the external table) in BigQuery. Now write a query to retrieve the PULocationID and DOLocationID on the same table. Why are the estimated number of Bytes different?**

```sql
SELECT COUNT( DISTINCT  PULocationID  )
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned`;
-- 155.12 MB
```
```sql
SELECT COUNT( DISTINCT PUlocationID  ), COUNT( DISTINCT DOlocationID  )
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned` ;
-- 310.24 MB
```
`BigQuery is a columnar database, and it only scans the specific columns requested in the query. Querying two columns (PULocationID, DOLocationID) requires reading more data than querying one column (PULocationID), leading to a higher estimated number of bytes processed.`

BigQuery is a columnar database, meaning it only scans the specific columns requested. Querying two columns (**PULocationID, DOLocationID**) requires reading more data than querying just one column (**PULocationID**), leading to a higher estimated number of bytes processed.

### Question 4: Option 4 => 8,333
**How many records have a fare_amount of 0?**

```sql
SELECT COUNT(fare_amount)
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned`
WHERE fare_amount = 0;
```
`8,333`

### Question 5: Option 1 => Partition by tpep_dropoff_datetime and cluster on VendorID
**What is the best strategy to make an optimized table in BigQuery if your query will always filter based on `tpep_dropoff_datetime` and order the results by `VendorID`?**  
**Create a new table with this strategy:**

```sql
CREATE OR REPLACE TABLE zoomcamp-450016.zoomcamp.yellow_tripdata_partitioned_clustered
PARTITION BY DATE(tpep_dropoff_datetime)
CLUSTER BY VendorID AS
SELECT * FROM zoomcamp-450016.zoomcamp.external_yellow_tripdata;
```

`Partition by tpep_dropoff_datetime and cluster on VendorID`

### Question 6: Option 1 => 310.24 MB for non-partitioned table and 26.84 MB for the partitioned table
**Write a query to retrieve the distinct VendorIDs between tpep_dropoff_datetime 2024-03-01 and 2024-03-15 (inclusive)**
**Use the materialized table you created earlier in your from clause and note the estimated bytes. Now change the table in the from clause to the partitioned table you created for question 5 and note the estimated bytes processed. What are these values?**
**Choose the answer which most closely matches.**  

```sql
SELECT DISTINCT VendorID
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_non_partitioned`
WHERE tpep_dropoff_datetime >= timestamp '2024-03-01 00:00:00'
  AND tpep_dropoff_datetime < timestamp '2024-03-16 00:00:00';
-- 310,24 MB

SELECT DISTINCT VendorID
FROM `zoomcamp-450016.zoomcamp.yellow_tripdata_partitioned_clustered`
WHERE tpep_dropoff_datetime >= timestamp '2024-03-01 00:00:00'
  AND tpep_dropoff_datetime < timestamp '2024-03-16 00:00:00';
-- 26,84 KB
```

`310.24 MB for non-partitioned table and 26.84 MB for the partitioned table`

### Question 7: Option 3 => GCP Bucket
**Where is the data stored in the External Table you created?**
`GCP Bucket`

### Question 8: Option 1 => False 
**It is best practice in Big Query to always cluster your data:**
`False`
