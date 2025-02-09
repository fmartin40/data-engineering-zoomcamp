# Module 1 Homework: Docker & SQL

Homework instructions for week1: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/01-docker-terraform/homework.md)  
Solutions: [link](https://github.com/DataTalksClub/data-engineering-zoomcamp/blob/main/cohorts/2025/01-docker-terraform/solution.md)
## Answer-Question 1: Option 1: 24.3.1

```bash
docker run -it --entrypoint bash python:3.12.8
pip --version
```

## Answer-Question 2: Option5: db:5432

## Answer-Question 3: Option 2: 104,802; 198,924; 109,603; 27,678; 35,189

```sql
SELECT count(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
    AND lpep_dropoff_datetime < '2019-11-01'
    AND trip_distance <= 1.0
UNION
SELECT count(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
    AND lpep_dropoff_datetime < '2019-11-01'
    AND trip_distance > 1.0
    AND trip_distance <= 3.0
UNION
SELECT count(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
    AND lpep_dropoff_datetime < '2019-11-01'
    AND trip_distance > 3.0
    AND trip_distance <= 7.0
UNION
SELECT count(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
    AND lpep_dropoff_datetime < '2019-11-01'
    AND trip_distance > 7.0
    AND trip_distance <= 10.0
UNION
SELECT count(*)
FROM public.green_taxi_trips
WHERE lpep_pickup_datetime >= '2019-10-01'
    AND lpep_dropoff_datetime < '2019-11-01'
    AND trip_distance > 10;
```

## Answer-Question 4: Option 4: - 2019-10-31

```sql
SELECT
    trip_distance,
    lpep_pickup_datetime
FROM
    public.green_taxi_trips
ORDER BY
    trip_distance DESC
```

## Answer-Question 5: Option 1: East Harlem North, East Harlem South, Morningside Heights

```sql
SELECT
    SUM(total_amount) as Total_Amount,
    z."Zone",
    z."Borough"
FROM
    public.green_taxi_trips as gtt
    JOIN public.zones as z ON gtt."PULocationID" = z."LocationID"
WHERE
    gtt.lpep_pickup_datetime::date = '2019-10-18'
GROUP BY
    z."Zone",
    z."Borough"
HAVING
    SUM(total_amount) > 13000
ORDER BY
    Total_Amount DESC;
```

## Answer-Question 6: Option 2: JFK Airport

```sql
SELECT
    zdo."Zone",
    gtt.tip_amount
FROM
    public.green_taxi_trips as gtt
    JOIN public.zones as zpu ON gtt."PULocationID" = zpu."LocationID"
    JOIN public.zones as zdo ON gtt."DOLocationID" = zdo."LocationID"
WHERE
    gtt.lpep_pickup_datetime::date >= '2019-10-01'
    AND gtt.lpep_pickup_datetime::date < '2019-11-01'
    AND zpu."Zone" = 'East Harlem North'
ORDER BY
    gtt.tip_amount DESC;
```

## Answer-Question 7: Option 4: - terraform init, terraform apply -auto-approve, terraform destroy
