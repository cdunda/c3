provider "aws" {
  region                      = "us-east-1"
  access_key                  = "mock_access_key"
  secret_key                  = "mock_secret_key"
  skip_credentials_validation = true
  skip_requesting_account_id  = true
  s3_use_path_style           = true
  endpoints {
    s3 = "http://localhost:4566"
  }
}

locals {
  deployments = {
    "0"  = ["deployhash112/index.html", "deployhash112/css/font.css", "deployhash112/images/hey.png"]
    "5"  = ["dsfsfsl9074/root.html", "dsfsfsl9074/styles/font.css", "dsfsfsl9074/img/hey.png"]
    "10" = ["delkjlkploy3/base.html", "delkjlkploy3/fonts/font.css", "delkjlkploy3/png/hey.png"]
  }
}

resource "aws_s3_bucket" "test_bucket" {
  bucket = "test-bucket"
}

resource "aws_s3_object" "deployments" {
  for_each = transpose(local.deployments)
  bucket   = aws_s3_bucket.test_bucket.id
  key      = each.key
  source   = ""

  # Mimic different deployment timestamps based off their key's value e.g. 10 seconds
  provisioner "local-exec" {
    command = <<EOT
        sleep ${each.value[0]}
        awslocal --endpoint-url=http://localhost:4566 s3api copy-object --bucket test-bucket --copy-source test-bucket/${each.key} --key ${each.key} --metadata-directive REPLACE
      EOT
  }
}
