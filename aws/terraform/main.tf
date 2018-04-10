provider "aws" {
  region     = "${var.aws_region}"
}

resource "aws_iam_role" "lambda-plaid-role" {
  name = "lambda-plaid-role"
  assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Action": "sts:AssumeRole",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Effect": "Allow",
      "Sid": ""
    }
  ]
}
EOF
}

data "aws_iam_policy_document" "lambda-plaid-role-policy-document" {
  statement {
    actions = [
      "ssm:GetParameter",
      "ssm:PutParameter"
    ]
    resources = [
      "arn:aws:ssm:*:*:parameter/*"
    ]
  }
  statement {
    actions = [
      "logs:CreateLogGroup",
      "logs:CreateLogStream",
      "logs:PutLogEvents"
    ]
    resources = [
      "arn:aws:logs:*:*:*"
    ]
  }
}

resource "aws_iam_policy" "lambda-plaid-role-policy" {
  name = "lambda-plaid-role-policy"
  path = "/"
  policy = "${data.aws_iam_policy_document.lambda-plaid-role-policy-document.json}"
}

resource "aws_iam_role_policy_attachment" "policy-attachment" {
  role = "${aws_iam_role.lambda-plaid-role.name}"
  policy_arn = "${aws_iam_policy.lambda-plaid-role-policy.arn}"
}

data "archive_file" "plaid-demo-1-zip" {
  type        = "zip"
  source_dir = "plaid-demo-1/"
  output_path = "plaid-demo-1.zip"
}

resource "aws_lambda_function" "lambda-plaid-demo-1" {
    filename = "${data.archive_file.plaid-demo-1-zip.output_path}"
    function_name = "plaid-demo-1"
    role = "${aws_iam_role.lambda-plaid-role.arn}"
    handler = "lambda_function.lambda_handler"
    runtime = "python3.6"
    timeout = 10
    source_code_hash = "${data.archive_file.plaid-demo-1-zip.output_base64sha256}"
}
