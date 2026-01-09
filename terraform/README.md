# Terraform Infrastructure

This directory contains Terraform configuration for deploying the NHS MESH client Lambda function to AWS.

## Prerequisites

- Terraform >= 1.0
- AWS CLI configured with appropriate credentials
- AWS account with permissions to create Lambda, S3, DynamoDB, IAM, and EventBridge resources

## Resources Created

- **Lambda Function**: Python 3.11 runtime with configurable timeout and memory
- **IAM Role**: Execution role with permissions for CloudWatch Logs, S3, and DynamoDB
- **S3 Bucket**: Encrypted storage for MESH messages with versioning enabled
- **DynamoDB Table**: Message tracking table with on-demand billing
- **CloudWatch Log Group**: Lambda function logs with 14-day retention
- **EventBridge Rule**: Scheduled trigger (every 15 minutes by default)

## Configuration

1. Copy the example variables file:
```bash
cp terraform.tfvars.example terraform.tfvars
```

2. Edit `terraform.tfvars` with your values:
```hcl
s3_bucket_name  = "your-unique-bucket-name"
mesh_mailbox_id = "your-mesh-mailbox-id"
mesh_password   = "your-mesh-password"
mesh_endpoint   = "INT"  # or "LIVE"
```

## Deployment

Initialize Terraform:
```bash
terraform init
```

Preview changes:
```bash
terraform plan
```

Apply configuration:
```bash
terraform apply
```

## Variables

| Variable | Description | Default | Required |
|----------|-------------|---------|----------|
| aws_region | AWS region | eu-west-2 | No |
| environment | Environment name | dev | No |
| s3_bucket_name | S3 bucket name | - | Yes |
| mesh_mailbox_id | MESH mailbox ID | - | Yes |
| mesh_password | MESH password | - | Yes |
| mesh_endpoint | MESH endpoint (INT/LIVE) | INT | No |
| lambda_function_name | Lambda function name | nhs-mesh-client | No |
| lambda_timeout | Timeout in seconds | 900 | No |
| lambda_memory_size | Memory in MB | 512 | No |
| batch_size | Messages per batch | 500 | No |

## Outputs

After deployment, Terraform outputs:
- Lambda function ARN and name
- S3 bucket name and ARN
- DynamoDB table name and ARN
- CloudWatch log group name

## State Management

For production use, configure remote state storage:

```hcl
terraform {
  backend "s3" {
    bucket = "your-terraform-state-bucket"
    key    = "mesh-client/terraform.tfstate"
    region = "eu-west-2"
  }
}
```

## Cleanup

To destroy all resources:
```bash
terraform destroy
```

**Warning**: This will delete all data in S3 and DynamoDB. Ensure backups exist before destroying.
