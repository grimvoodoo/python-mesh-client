data "archive_file" "lambda_zip" {
  type        = "zip"
  source_dir  = "${path.module}/../src"
  output_path = "${path.module}/lambda_function.zip"
}

resource "aws_lambda_function" "mesh_client" {
  filename         = data.archive_file.lambda_zip.output_path
  function_name    = var.lambda_function_name
  role            = aws_iam_role.lambda_execution_role.arn
  handler         = "lambda_function.lambda_handler"
  source_code_hash = data.archive_file.lambda_zip.output_base64sha256
  runtime         = "python3.11"
  timeout         = var.lambda_timeout
  memory_size     = var.lambda_memory_size

  environment {
    variables = {
      MESH_MAILBOX_ID     = var.mesh_mailbox_id
      MESH_PASSWORD       = var.mesh_password
      MESH_ENDPOINT       = var.mesh_endpoint
      S3_BUCKET_NAME      = aws_s3_bucket.mesh_messages.id
      DYNAMODB_TABLE_NAME = aws_dynamodb_table.mesh_tracking.name
      BATCH_SIZE          = var.batch_size
    }
  }

  depends_on = [
    aws_iam_role_policy.lambda_policy
  ]
}

resource "aws_cloudwatch_log_group" "lambda_logs" {
  name              = "/aws/lambda/${var.lambda_function_name}"
  retention_in_days = 14
}
