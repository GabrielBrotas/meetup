resource "aws_cognito_user_pool" "user_pool" {
  name = "${var.project_name}-pool"
  
  password_policy {
    minimum_length = 6
  }

  schema {
    name                     = "email"
    attribute_data_type      = "String"
    developer_only_attribute = false
    mutable                  = true
    required                 = true

    string_attribute_constraints {
      min_length = 1
      max_length = 256
    }
  }

  tags = {
    Owner: "Gabriel",
    Project: "${var.project_name}",
    Environment: "${var.environment}"
  }
}

resource "aws_cognito_user_pool_client" "client" {
  name = "${var.project_name}-pool-client"

  user_pool_id = aws_cognito_user_pool.user_pool.id
  generate_secret = false
  refresh_token_validity = 90
  prevent_user_existence_errors = "ENABLED"
  
  explicit_auth_flows = [
    "ALLOW_REFRESH_TOKEN_AUTH",
    "ALLOW_USER_PASSWORD_AUTH",
    "ALLOW_ADMIN_USER_PASSWORD_AUTH"
  ]

  read_attributes = [ "email" ]

}

output "cognito_client_id" {
    value = aws_cognito_user_pool.user_pool.id
}

output "cognito_app_client_id" {
    value = aws_cognito_user_pool_client.client.id
}