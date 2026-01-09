output "lambda_function_arn" {
  description = "ARN of the Lambda function"
  value       = aws_lambda_function.mesh_client.arn
}

output "lambda_function_name" {
  description = "Name of the Lambda function"
  value       = aws_lambda_function.mesh_client.function_name
}

output "s3_bucket_name" {
  description = "Name of the S3 bucket for messages"
  value       = aws_s3_bucket.mesh_messages.id
}

output "s3_bucket_arn" {
  description = "ARN of the S3 bucket"
  value       = aws_s3_bucket.mesh_messages.arn
}

output "dynamodb_table_name" {
  description = "Name of the DynamoDB table"
  value       = aws_dynamodb_table.mesh_tracking.name
}

output "dynamodb_table_arn" {
  description = "ARN of the DynamoDB table"
  value       = aws_dynamodb_table.mesh_tracking.arn
}

output "cloudwatch_log_group" {
  description = "CloudWatch log group for Lambda"
  value       = aws_cloudwatch_log_group.lambda_logs.name
}
