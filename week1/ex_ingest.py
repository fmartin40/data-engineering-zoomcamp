import pandas as pd
import pyarrow.parquet as pq
from sqlalchemy import create_engine
from time import time
import argparse
import os

def extract(file_path):
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"The file {file_path} does not exist.")
    return pq.ParquetFile(file_path)

def transform(parquet_file):
    return parquet_file.schema.names

def load(parquet_file, columns, engine, table_name):
    start_time = time()
    num_row_groups = parquet_file.num_row_groups

    for i in range(num_row_groups):
        chunk = parquet_file.read_row_group(i, columns=columns)
        df_chunk = chunk.to_pandas()
        df_chunk.to_sql(name=table_name, con=engine, if_exists='append', index=False)
        print(f"Inserted row group {i + 1} of {num_row_groups}")

    end_time = time()
    print(f"Ingestion completed. Total time: {end_time - start_time:.2f} seconds")

def create_table_schema(engine, table_name, parquet_file):
    df_sample = pd.read_parquet(parquet_file, engine='pyarrow').head(0)
    df_sample.to_sql(name=table_name, con=engine, if_exists='replace', index=False)

def main(params):
    connection_string = f'postgresql://{params.user}:{params.password}@{params.host}:{params.port}/{params.db}'
    engine = create_engine(connection_string)

    parquet_file = extract(params.parquet_file)
    columns = transform(parquet_file)
    create_table_schema(engine, params.table_name, params.parquet_file)
    load(parquet_file, columns, engine, params.table_name)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest Parquet data to Postgres')
    parser.add_argument('--user', help='Database user')
    parser.add_argument('--password', help='Database password')
    parser.add_argument('--host', help='Database host')
    parser.add_argument('--port', help='Database port')
    parser.add_argument('--db', help='Database name')
    parser.add_argument('--table_name', help='Name of the table to write results to')
    parser.add_argument('--parquet_file', help='Path to the Parquet file')

    args = parser.parse_args()
    main(args)