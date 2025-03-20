# GDPR Obfuscator tool

## Overview

This project provides a pythonic function to obfuscate specified PII fields in a CSV file stored in an S3 bucket. The main function `lambda_handler` is designed to be used as an AWS Lambda function. It reads a CSV file from an S3 bucket, obfuscates the specified PII fields, and writes the obfuscated file back to the S3 bucket.

## Prerequisites

- AWS account with s3 and lambda functions

## Setup


### Create Lambda Function with the AWS Lambda Console Instructions

1. **Create a Lambda Function:**
   - Go to the AWS Lambda console.
   - Click on "Create function".
   - Choose "Author from scratch".
   - Enter a function name.
   - Choose "Python 3.12" as the runtime and "x86_64" architecture.
   - Click "Create function".

2. **Add Permissions to the AWS Bucket for the Lambda Function:**
   - Go to the IAM console, click on "Policies" in the left-hand menu (under access management).
   - Attach the `AmazonS3FullAccess` AWS managed policy to the Lambda execution role.

3. **Upload the Code:**
   - Download the zip file named "lambda_function.zip" found in the codebase (obfuscator/lambda_function.zip).
   - In the Lambda console, upload the zip file in the code source section.

4. **Create a Layer Compatible with the Lambda Runtime (Python 3.12):**
   - In the Lambda console, click on "Layers" in the left-hand menu (under additional resources).
   - Click "Create layer".
   - Enter a name for the layer.
   - Upload the zip file named "lambda_layer.zip" found in the codebase (obfuscator/lambda_layer.zip).
   - Choose "Python 3.12" as a compatible runtime.
   - Click "Create".

5. **Add the Layer to Your Lambda Function:**
   - In the Lambda console, go to your Lambda function.
   - In the "Layers" section at the bottom of the Code tab, click "Add a layer".
   - Choose "Custom layers".
   - Select the layer and version you created.
   - Click "Add".

6. **Set the Timeout:**
   - In the Lambda function configuration tab, increase the timeout to a high enough number to ensure the function has enough time to process your large files.

## Usage Instructions

### Event Data

The `lambda_handler` function expects the following event data:

- `file_to_obfuscate` (str): S3 URI of the file to be obfuscated.
- `pii_fields` (list): List of column names in the CSV file that need to be obfuscated.

### Example Event

```json
{
  "file_to_obfuscate": "s3://my_ingestion_bucket/new_data/file1.csv",
  "pii_fields": ["name", "email_address"]
}
```

### Output

The output of the obfuscation tool will be a new CSV file, of the input file with the specified PII fields obfuscated, found in the same S3 location as the input with the suffix '_obfuscated'. 

## Running the tests in Terminal

1. **Run the following command** to clone the repository in your terminal:

    ```sh
    git clone https://github.com/H1drogen/gdpr_obfuscator.git
    ```

3. **Navigate into the cloned repository**:

    ```sh
    cd gdpr_obfuscator
    ```

2. **Ensure you have `python` and `poetry` installed**. Install the poetry dependencies into current python interpreter by:
    ```sh
    poetry update
    env activate
    ```

3. Make sure your python path is set correctly with
    ```sh
    export PYTHONPATH=$PYTHONPATH:/path/to/your/project
    ```

5. **Run the tests** using the following command:
    ```sh
    poetry run pytest tests/test_lambda_function.py
    ```
