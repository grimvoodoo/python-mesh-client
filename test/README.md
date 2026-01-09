# Local Testing

This directory contains scripts for developing and testing the NHS MESH client logic locally before deploying to AWS Lambda.

## Setup

1. Install dependencies:
```bash
pip install -r test/requirements.txt
```

2. Configure environment variables:
```bash
cp test/.env.example test/.env
# Edit test/.env with your MESH credentials
```

3. Load environment variables (if using .env file):
```bash
export $(cat test/.env | xargs)
```

## Running Tests

Execute the test script:
```bash
python test/mesh_client_test.py
```

Or make it executable and run directly:
```bash
chmod +x test/mesh_client_test.py
./test/mesh_client_test.py
```

## What It Does

The test script simulates the Lambda function workflow:

1. **Initialize MESH client** with credentials from environment variables
2. **List messages** available in the mailbox
3. **Process in batches** of 500 messages (configurable)
4. **Download messages** and extract metadata
5. **Save results** to local files (simulating S3 storage)
6. **Acknowledge messages** to remove from queue

## Output

Test results are saved to `test/output/` directory:
- Each batch creates a JSON file: `batch-{timestamp}-{batch_number}.json`
- Files contain message metadata and processing status

## Mock Mode

By default, the script runs in mock mode with simulated data. To test with actual MESH API:

1. Uncomment the MESH client initialization code
2. Uncomment the actual API calls in each function
3. Ensure your credentials and certificates are configured correctly

## Development Workflow

1. Develop logic in `mesh_client_test.py`
2. Test locally with mock data
3. Test with actual MESH integration endpoint
4. Once validated, copy logic to `src/lambda_function.py`
5. Add AWS-specific code (S3, DynamoDB)
6. Deploy via Terraform

## Environment Variables

| Variable | Description | Required |
|----------|-------------|----------|
| MESH_MAILBOX_ID | MESH mailbox identifier | Yes |
| MESH_PASSWORD | MESH mailbox password | Yes |
| MESH_ENDPOINT | INT or LIVE | Yes |
| MESH_CERT_FILE | Path to certificate PEM | Yes |
| MESH_KEY_FILE | Path to key PEM | Yes |
| BATCH_SIZE | Messages per batch | No (default: 500) |

## Troubleshooting

### Certificate Issues
- Ensure certificate paths are absolute
- Verify PEM format for both cert and key
- Check file permissions (readable by current user)

### Connection Issues
- Verify MESH endpoint is accessible
- Check network connectivity
- Confirm mailbox credentials are correct

### Mock Data
- The script uses 149 mock messages for testing
- Adjust mock data in `list_messages()` function as needed
