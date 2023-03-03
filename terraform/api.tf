
resource "aws_iam_role_policy_attachment" "lambda_policy" {
  role       = aws_iam_role.lambda_exec.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_apigatewayv2_api" "lambda_api" {
  name          = "api_gw_lambda_adn"
  protocol_type = "HTTP"
}

resource "aws_apigatewayv2_stage" "lambda_api" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  name        = "api_gw_lambda"
  auto_deploy = true

  access_log_settings {
    destination_arn = aws_cloudwatch_log_group.api_gw.arn

    format = jsonencode({
      requestId               = "$context.requestId"
      sourceIp                = "$context.identity.sourceIp"
      requestTime             = "$context.requestTime"
      protocol                = "$context.protocol"
      httpMethod              = "$context.httpMethod"
      resourcePath            = "$context.resourcePath"
      routeKey                = "$context.routeKey"
      status                  = "$context.status"
      responseLength          = "$context.responseLength"
      integrationErrorMessage = "$context.integrationErrorMessage"
      }
    )
  }
}

resource "aws_apigatewayv2_integration" "lambda_call" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  integration_uri    = aws_lambda_function.lambda_adn_function.invoke_arn
  integration_type   = "AWS_PROXY"
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "get_stats" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  route_key = "GET /stats"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_call.id}"
}

resource "aws_apigatewayv2_route" "post_mutation" {
  api_id = aws_apigatewayv2_api.lambda_api.id

  route_key = "POST /mutation"
  target    = "integrations/${aws_apigatewayv2_integration.lambda_call.id}"
}

resource "aws_cloudwatch_log_group" "api_gw" {
  name = "/aws/api_gw/${aws_apigatewayv2_api.lambda_api.name}"

  retention_in_days = 30
}

resource "aws_lambda_permission" "api_gw" {
  statement_id  = "AllowExecutionFromAPIGateway"
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.lambda_adn_function.function_name
  principal     = "apigateway.amazonaws.com"

  source_arn = "${aws_apigatewayv2_api.lambda_api.execution_arn}/*/*"
}
