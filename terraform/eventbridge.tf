resource "aws_cloudwatch_event_rule" "mesh_poll_schedule" {
  name                = "${var.lambda_function_name}-schedule"
  description         = "Trigger MESH client Lambda every 15 minutes"
  schedule_expression = "rate(15 minutes)"
}

resource "aws_cloudwatch_event_target" "lambda_target" {
  rule      = aws_cloudwatch_event_rule.mesh_poll_schedule.name
  target_id = "MeshClientLambda"
  arn       = aws_lambda_function.mesh_client.arn
}

resource "aws_lambda_permission" "allow_eventbridge" {
  statement_id  = "AllowExecutionFromEventBridge"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.mesh_client.function_name
  principal     = "events.amazonaws.com"
  source_arn    = aws_cloudwatch_event_rule.mesh_poll_schedule.arn
}
