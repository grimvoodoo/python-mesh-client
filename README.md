# NHS MESH Mailbox Client

A Python AWS Lambda function that retrieves messages from an NHS MESH (Message Exchange for Social Care and Health) mailbox, stores them in S3, and tracks their status in DynamoDB.

## Overview

This Lambda function automates the process of:
- Connecting to an NHS MESH mailbox
- Checking for available messages
- Downloading messages in batches of up to 500
- Storing message content in S3
- Recording message metadata in DynamoDB
- Acknowledging message receipt to clear them from the MESH queue

## Architecture

```
NHS MESH Mailbox → Lambda Function → S3 Bucket (messages)
                                   → DynamoDB (tracking)
```

### Processing Flow

1. **Check mailbox**: Query MESH API for available messages
2. **Batch processing**: Download messages in batches (max 500 per batch)
3. **Store messages**: Save each batch to S3 as a separate file
4. **Track metadata**: Create DynamoDB entries with:
   - `message_id`: Unique MESH message identifier
   - `timestamp`: Processing timestamp
   - `status`: Set to "received"
5. **Acknowledge**: Send read acknowledgment to MESH to remove messages from queue
6. **Loop**: Repeat until all messages are processed

## MESH Client Library

This project uses the official [NHS Digital MESH client library](https://github.com/NHSDigital/mesh-client) to interact with the MESH API.

## Requirements

### AWS Resources

- **Lambda Function**: Python runtime (3.9+)
- **S3 Bucket**: For storing downloaded messages
- **DynamoDB Table**: For message tracking with schema:
  - Primary Key: `message_id` (String)
  - Attributes: `timestamp` (String/Number), `status` (String)
- **IAM Role**: Lambda execution role with permissions for:
  - S3: `s3:PutObject`
  - DynamoDB: `dynamodb:PutItem`
  - CloudWatch Logs: `logs:CreateLogGroup`, `logs:CreateLogStream`, `logs:PutLogEvents`
  - VPC access (if MESH requires VPC)

### NHS MESH Requirements

- MESH mailbox ID
- MESH mailbox password
- Client certificate and key files (PEM format)
- Network connectivity to MESH API (may require VPC configuration)
- Choose endpoint: `INT_ENDPOINT` (integration/testing) or `LIVE_ENDPOINT` (production)

## Environment Variables

Configure the following environment variables in your Lambda function:

```
MESH_MAILBOX_ID       - Your MESH mailbox identifier
MESH_PASSWORD         - MESH mailbox password
MESH_ENDPOINT         - MESH endpoint (INT or LIVE)
MESH_CERT_FILE        - Path to client certificate PEM file
MESH_KEY_FILE         - Path to client key PEM file
S3_BUCKET_NAME        - Target S3 bucket name
DYNAMODB_TABLE_NAME   - DynamoDB table name for tracking
BATCH_SIZE            - Max messages per batch (default: 500)
```

## Installation

### Python Dependencies

Create a `requirements.txt`:

```
mesh-client>=2.0.0
boto3>=1.26.0
```

**Note**: The `mesh-client` library handles all MESH API communication, including authentication and message operations.

### Deployment

1. Package the Lambda function with dependencies:
```bash
pip install -r requirements.txt -t .
zip -r function.zip .
```

2. Deploy via AWS CLI:
```bash
aws lambda create-function \
  --function-name nhs-mesh-client \
  --runtime python3.9 \
  --role arn:aws:iam::YOUR_ACCOUNT:role/lambda-execution-role \
  --handler lambda_function.lambda_handler \
  --zip-file fileb://function.zip \
  --timeout 900 \
  --memory-size 512
```

3. Configure environment variables (see above)

## Usage

### Scheduled Execution

Configure EventBridge (CloudWatch Events) to trigger the Lambda on a schedule:

```bash
aws events put-rule \
  --name nhs-mesh-poll \
  --schedule-expression "rate(15 minutes)"

aws lambda add-permission \
  --function-name nhs-mesh-client \
  --statement-id nhs-mesh-poll \
  --action lambda:InvokeFunction \
  --principal events.amazonaws.com \
  --source-arn arn:aws:events:REGION:ACCOUNT:rule/nhs-mesh-poll
```

### Manual Invocation

```bash
aws lambda invoke \
  --function-name nhs-mesh-client \
  --payload '{}' \
  output.json
```

## Batch Processing Logic

The function processes messages in batches to comply with API limits and optimize performance:

1. Initialize MESH client using the `mesh-client` library
2. List available message IDs using `client.list_messages()`
3. Split into chunks of 500 messages
4. For each chunk:
   - Download each message using `client.retrieve_message(message_id)`
   - Store messages to S3 (individual files or batched)
   - Write metadata entries to DynamoDB
   - Acknowledge each message using `client.acknowledge_message(message_id)`
5. Continue until all messages are processed

### Example MESH Client Usage

```python
from mesh_client import MeshClient, INT_ENDPOINT, LIVE_ENDPOINT

# Initialize client
with MeshClient(
    INT_ENDPOINT,  # or LIVE_ENDPOINT for production
    'MYMAILBOX',
    'Password',
    cert=('/path/to/cert.pem', '/path/to/key.pem')
) as client:
    # List messages
    messages = client.list_messages()
    
    # Retrieve a message
    message = client.retrieve_message(message_id)
    
    # Acknowledge message
    client.acknowledge_message(message_id)
```

## DynamoDB Schema

**Table Name**: `mesh-messages` (or as configured)

| Attribute | Type | Description |
|-----------|------|-------------|
| message_id | String (PK) | Unique MESH message identifier |
| timestamp | String | ISO 8601 timestamp of processing |
| status | String | Message status (initially "received") |
| batch_id | String (optional) | Batch identifier for grouping |
| s3_key | String (optional) | S3 object key where message is stored |

## S3 Storage Structure

Messages are stored with the following key structure:

```
mesh-messages/
  └── YYYY/MM/DD/
      └── batch-{timestamp}-{batch_number}.json
```

## Error Handling

- **Network errors**: Retry with exponential backoff
- **API rate limits**: Implement appropriate delays between batches
- **Partial failures**: Track successfully processed messages to avoid reprocessing
- **DynamoDB throttling**: Implement batch writes with error handling

## Monitoring

Monitor the Lambda function using:
- **CloudWatch Logs**: Function execution logs
- **CloudWatch Metrics**: Invocation count, duration, errors
- **DynamoDB Metrics**: Write capacity, throttling
- **S3 Metrics**: Object count, storage size

## Security Considerations

- Store MESH credentials in AWS Secrets Manager
- Enable encryption at rest for S3 and DynamoDB
- Use VPC endpoints for AWS service access
- Implement least-privilege IAM policies
- Enable CloudTrail logging for audit trail

## License

See `LICENSE` file for details.

## Support

For NHS MESH API documentation and support, refer to the official NHS Digital documentation.
