from io import BytesIO

import boto3
import pandas as pd
from moto import mock_aws
import pytest

from obfuscator.main import lambda_handler


@pytest.fixture
def test_s3_setup():
    with mock_aws():
        s3 = boto3.client('s3', region_name='us-east-1')
        bucket_name = 'my_ingestion_bucket'
        s3.create_bucket(Bucket=bucket_name)

        csv_data = """student_id,name,course,cohort,graduation_date,email_address
        1234,John Smith,Software,2024-03-31,j.smith@email.com"""
        s3.put_object(Bucket=bucket_name, Key='new_data/file1.csv', Body=csv_data)
        yield s3

def test_lambda_handler_obfuscates_pii_fields(test_s3_setup):
    event = {
        'file_to_obfuscate': 's3://my_ingestion_bucket/new_data/file1.csv',
        'pii_fields': ['name', 'email_address']
    }

    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert 'File obfuscated and saved to s3://my_ingestion_bucket/new_data/file1_obfuscated.csv' in response['body']

    obfuscated_obj = test_s3_setup.get_object(Bucket='my_ingestion_bucket', Key='new_data/file1_obfuscated.csv')['Body'].read()
    df_obfuscated = pd.read_csv(BytesIO(obfuscated_obj))

    assert df_obfuscated['name'].iloc[0] == '***'
    assert df_obfuscated['email_address'].iloc[0] == '***'

def test_lambda_handler_handles_empty_pii_fields(test_s3_setup):
    event = {
        'file_to_obfuscate': 's3://my_ingestion_bucket/new_data/file1.csv',
        'pii_fields': []
    }

    context = {}

    response = lambda_handler(event, context)

    assert response['statusCode'] == 200
    assert 'File obfuscated and saved to s3://my_ingestion_bucket/new_data/file1_obfuscated.csv' in response['body']

    obfuscated_obj = test_s3_setup.get_object(Bucket='my_ingestion_bucket', Key='new_data/file1_obfuscated.csv')['Body'].read()
    df_obfuscated = pd.read_csv(BytesIO(obfuscated_obj))

    assert df_obfuscated['name'].iloc[0] == 'John Smith'
    assert df_obfuscated['email_address'].iloc[0] == 'j.smith@email.com'
