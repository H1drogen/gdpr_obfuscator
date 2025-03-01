import boto3
import pandas as pd
from io import BytesIO

def lambda_handler(event, context):
    s3 = boto3.client('s3')
    bucket_name = event['file_to_obfuscate'].split('/')[2]
    file_name = '/'.join(event['file_to_obfuscate'].split('/')[3:])
    file_path = f'/tmp/{file_name}'
    obj = s3.get_object(Bucket=bucket_name, Key=file_name)['Body'].read()
    df = pd.read_csv(BytesIO(obj))
    for col in event['pii_fields']:
        df[col] = '***'
    s3.put_object(Bucket=bucket_name, Key=file_name.replace('.csv', '_obfuscated.csv'), Body=df.to_csv(index=False))
    return {
        'statusCode': 200,
        'body': f'File obfuscated and saved to s3://{bucket_name}/{file_name.replace(".csv", "_obfuscated.csv")}'
    }
