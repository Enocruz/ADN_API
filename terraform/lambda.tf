
data "archive_file" "lambda_adn_function" {
  type = "zip"

  source_dir  = "../src"
  output_path = "lambda_function.zip"
}

# to Create function
resource "aws_lambda_function" "lambda_adn_function" {
  function_name    = "lambda_adn_function"
  filename         = "lambda_function.zip"
  runtime          = "python3.9"
  handler          = "index.handler"
  source_code_hash = data.archive_file.lambda_adn_function.output_base64sha256
  role             = aws_iam_role.lambda_exec.arn
}

resource "aws_cloudwatch_log_group" "lambda_adn_function" {
  name              = "/aws/lambda/lambda_adn_function"
  retention_in_days = 3
}

resource "aws_iam_role" "lambda_exec" {
  name = "lambda_iam_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action = "sts:AssumeRole"
      Effect = "Allow"
      Sid    = ""
      Principal = {
        Service = "lambda.amazonaws.com"
      }
      }
    ]
  })
}
