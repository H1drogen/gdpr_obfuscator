"""
Module provides a function to obfuscate specified PII fields in a CSV file stored in an S3 bucket.

The main function `lambda_handler` is designed to be used as an AWS Lambda function. It reads a CSV file from
an S3 bucket, obfuscates the specified PII fields, and writes the obfuscated file back to the S3 bucket.
"""

from io import BytesIO, StringIO
import boto3
import pandas as pd



def lambda_handler(event, context):
    """
    AWS Lambda function to obfuscate specified PII fields in a CSV file stored in an S3 bucket.

    Parameters:
    event (dict): Event data passed to the function, expected to contain:
        - 'file_to_obfuscate' (str): S3 URI of the file to be obfuscated.
        - 'pii_fields' (list): List of column names in the CSV file that need to be obfuscated.
    context (object): AWS Lambda context object (not used in this function).

    Returns:
    dict: Response object containing:
        - 'statusCode' : HTTP status code indicating the result of the operation.
        - 'body' : Message indicating the outcome of the obfuscation process.
    """
    s3 = boto3.client('s3')
    bucket_name = event['file_to_obfuscate'].split('/')[2]
    file_name = '/'.join(event['file_to_obfuscate'].split('/')[3:])
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)['Body']
    df = pd.read_csv(obj)
    for col in event['pii_fields']:
        df[col] = '***'
    s3.put_object(Bucket=bucket_name, Key=file_name.replace('.csv', '_obfuscated.csv'),
                  Body=df.to_csv(index=False))
    new_file_path = file_name.replace('.csv', '_obfuscated.csv')
    return {
        'statusCode': 200,
        'body': f'File obfuscated and saved to s3://{bucket_name}/{new_file_path}'
    }
