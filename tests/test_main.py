import boto3
import pandas as pd
from moto import mock_aws
import pytest

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
