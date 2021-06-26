from ssm_parameter_store import EC2ParameterStore
import psycopg2
import boto3
import os

ENDPOINT="rdsinfinitelambda.cwm6fxdpl9ho.ap-southeast-1.rds.amazonaws.com"
PORT = "5432"
REGION="ap-southeast-1"
DBNAME="rdsinfinitelambda"

def connect():
    conn = None
    store = EC2ParameterStore(
        region_name = REGION
    )

    parameter = store.get_parameters_by_path('/cp/prod/app/database/', recursive=True)
    USR = parameter['master_user']
    PASSWORD = parameter['master_password']
    try:

        print('Connecting to the PostgreSQL database...')
        conn = psycopg2.connect(host=ENDPOINT, port=PORT, database=DBNAME, user=USR, password=PASSWORD)

        cur = conn.cursor()

        print('PostgreSQL database version:')
        cur.execute('SELECT version()')

        db_version = cur.fetchone()
        print(db_version)

        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
