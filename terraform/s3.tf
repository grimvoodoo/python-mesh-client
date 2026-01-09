resource "aws_s3_bucket" "mesh_messages" {
  bucket = var.s3_bucket_name
}

resource "aws_s3_bucket_versioning" "mesh_messages" {
  bucket = aws_s3_bucket.mesh_messages.id

  versioning_configuration {
    status = "Enabled"
  }
}

resource "aws_s3_bucket_server_side_encryption_configuration" "mesh_messages" {
  bucket = aws_s3_bucket.mesh_messages.id

  rule {
    apply_server_side_encryption_by_default {
      sse_algorithm = "AES256"
    }
  }
}

resource "aws_s3_bucket_public_access_block" "mesh_messages" {
  bucket = aws_s3_bucket.mesh_messages.id

  block_public_acls       = true
  block_public_policy     = true
  ignore_public_acls      = true
  restrict_public_buckets = true
}
