package s3

deny[msg] {
  input.resource_type == "aws_s3_bucket"
  input.acl == "public-read"
  msg = sprintf("S3 bucket %v must not be public", [input.name])
}
