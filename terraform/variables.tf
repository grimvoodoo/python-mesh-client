variable "aws_region" {
  description = "AWS region to deploy resources"
  type        = string
  default     = "eu-west-2"
}

variable "environment" {
  description = "Environment name (e.g., dev, staging, prod)"
  type        = string
  default     = "dev"
}

variable "lambda_function_name" {
  description = "Name of the Lambda function"
  type        = string
  default     = "nhs-mesh-client"
}

variable "lambda_timeout" {
  description = "Lambda function timeout in seconds"
  type        = number
  default     = 900
}

variable "lambda_memory_size" {
  description = "Lambda function memory size in MB"
  type        = number
  default     = 512
}

variable "s3_bucket_name" {
  description = "S3 bucket name for storing MESH messages"
  type        = string
}

variable "dynamodb_table_name" {
  description = "DynamoDB table name for message tracking"
  type        = string
  default     = "mesh-messages"
}

variable "mesh_mailbox_id" {
  description = "MESH mailbox identifier"
  type        = string
  sensitive   = true
}

variable "mesh_password" {
  description = "MESH mailbox password"
  type        = string
  sensitive   = true
}

variable "mesh_endpoint" {
  description = "MESH endpoint (INT or LIVE)"
  type        = string
  default     = "INT"
}

variable "batch_size" {
  description = "Maximum number of messages to process per batch"
  type        = number
  default     = 500
}
