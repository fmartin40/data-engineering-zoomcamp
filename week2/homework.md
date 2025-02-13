# Module 2 Homework: Workflow Orchestration

Homework instructions for week2: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/02-workflow-orchestration/homework.md)  
Solutions: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/02-workflow-orchestration/solution.md)  


I checked on my bucket the size of the file yellow_tripdata_2020-12.csv and the answer is 128.3 MB.

## Answer-Question 2: Option2: green_tripdata_2020-04.csv

## Answer-Question 3: Option2: 24,648,499

```sql
SELECT COUNT(*) 
FROM `trip_data_all.yellow_tripdata` 
WHERE filename LIKE 'yellow_tripdata_2020%';
```

## Answer-Question 4: Option3: 1,734,051

```sql
SELECT COUNT(*) 
FROM `trip_data_all.green_tripdata` 
WHERE filename LIKE 'green_tripdata_2020%';
```

## Answer-Question 5: Option3: 1,925,152

In this case, we first use the flow 06_gcp_taxi_scheduled and run a backfill execution.
Once the data was ingested on BigQuery, we can query it like the both below :

```sql
SELECT COUNT(*) 
FROM `rip_data_all.yellow_tripdata` 
WHERE filename LIKE 'yellow_tripdata_2021-03%';
```

## Answer-Question 6: Option2: America/New_York

AnswerIn the description of the timezone in Kestra, they specify that the timezone identifier is the second column in the Wikipedia table. When we check this table, we get this:

So, the answer is America/New_York.

