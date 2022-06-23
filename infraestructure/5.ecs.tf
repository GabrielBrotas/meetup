resource "aws_ecs_cluster" "ecs_cluster" {
  name = "${var.project_name}-cluster"

  setting {
    name  = "containerInsights"
    value = "enabled"
  }
}


resource "aws_iam_role" "ecs_task_role" {
    name = "${var.project_name}-ecs-api-role"
    path = "/"

    assume_role_policy = <<EOF
{
  "Version": "2012-10-17",
  "Statement": [
  {
    "Action": "sts:AssumeRole",
    "Principal": {
      "Service": "ecs-tasks.amazonaws.com"
    },
    "Effect": "Allow",
    "Sid": "ECSTaskAssumeRole"
  }
  ]
}
EOF
}

resource "aws_iam_policy" "ecs_api_policy" {
    name = "${var.project_name}-ecs-api-policy"
    path = "/"
    description = "IAM Policy to API"
    policy = data.aws_iam_policy_document.api_policy_document.json
}

data "aws_iam_policy_document" "api_policy_document" {
    statement {
      sid = "AllowECRPull"
      actions = [ "ecr:*" ]
      resources = [ 
        "${aws_ecr_repository.users_api.arn}",
        "${aws_ecr_repository.categories_api.arn}",
        "${aws_ecr_repository.meetings_api.arn}",

      ]
    }

    statement {
        actions = [ 
            "ecr:GetAuthorizationToken",
            "ecr:BatchCheckLayerAvailability",
            "ecr:GetDownloadUrlForLayer",
            "ecr:BatchGetImage",
            "logs:CreateLogStream",
            "logs:PutLogEvents",
        ]
        resources = [ "*" ]
    }

    statement {
        sid = "AllowCloudWatchLogs"
        actions = [ "logs:*" ]
        resources = [ "*" ]
    }
}

resource "aws_iam_policy_attachment" "ecs_api_policy_attachement" {
    name = "${var.project_name}-ecs-api-policy-attachement"
    roles = [aws_iam_role.ecs_task_role.name]
    policy_arn = aws_iam_policy.ecs_api_policy.arn
}

resource "aws_ecs_task_definition" "ecs_users_task_definition" {
    family = "${var.project_name}-ecs-users-td"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 256
    memory = 512
    execution_role_arn = aws_iam_role.ecs_task_role.arn
    task_role_arn = aws_iam_role.ecs_task_role.arn
    
    container_definitions = jsonencode([
        {
            "name" = "${var.project_name}-users",
            "image" = "${aws_ecr_repository.users_api.repository_url}:latest",
            "portMappings" = [
                {
                    "containerPort" = 4000
                }
            ],
            "environment" = [
                {
                    "name" = "COGNITO_CLIENT_ID",
                    "value" = "${aws_cognito_user_pool.user_pool.id}",
                },
                {
                    "name" = "COGNITO_APP_CLIENT_ID",
                    "value" = "${aws_cognito_user_pool_client.client.id}",
                }
            ]
        }
    ])
}

resource "aws_ecs_task_definition" "ecs_categories_task_definition" {
    family = "${var.project_name}-ecs-categories-td"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 256
    memory = 512
    execution_role_arn = aws_iam_role.ecs_task_role.arn
    task_role_arn = aws_iam_role.ecs_task_role.arn
    
    container_definitions = jsonencode([
        {
            "name" = "${var.project_name}-categories",
            "image" = "${aws_ecr_repository.categories_api.repository_url}:latest",
            "portMappings" = [
                {
                    "containerPort" = 4001
                }
            ],
            "environment" = [
                {
                    "name" = "ENVIRONMENT",
                    "value" = "prod",
                }
            ]
        }
    ])
}

resource "aws_ecs_task_definition" "ecs_meetings_task_definition" {
    family = "${var.project_name}-ecs-meetings-td"
    requires_compatibilities = ["FARGATE"]
    network_mode = "awsvpc"
    cpu = 256
    memory = 512
    execution_role_arn = aws_iam_role.ecs_task_role.arn
    task_role_arn = aws_iam_role.ecs_task_role.arn
    
    container_definitions = jsonencode([
        {
            "name" = "${var.project_name}-meetings",
            "image" = "${aws_ecr_repository.meetings_api.repository_url}:latest",
            "portMappings" = [
                {
                    "containerPort" = 4002
                }
            ],
            "environment" = [
                {
                    "name" = "ENVIRONMENT",
                    "value" = "prod",
                }
            ]
        }
    ])
}

resource "aws_security_group" "api_app_sg" {
    name = "${var.project_name}-api-app-sg"
    description = "Allow traffic from alb to api"
    vpc_id = module.vpc.vpc_id

    ingress = [
        {
            description = "Allow traffic from alb"
            from_port = 4000
            to_port = 4002
            protocol = "tcp"
            cidr_blocks = []
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = [aws_security_group.api_alb_sg.id]
            self = false
        }
    ]

    egress = [
        {
            description = "Allow all outbound traffic"
            from_port = 0
            to_port = 0
            protocol = "-1"
            cidr_blocks = ["0.0.0.0/0"]
            ipv6_cidr_blocks = []
            prefix_list_ids = []
            security_groups = []
            self = false
        }
    ]

    tags = {
        Name = "${var.project_name}-api-app-sg"
        Environment = "${var.project_name}"
    }
}

resource "aws_ecs_service" "users_ecs_service" {
    name = "${var.project_name}-ecs-users-service"
    cluster = aws_ecs_cluster.ecs_cluster.id
    task_definition = aws_ecs_task_definition.ecs_users_task_definition.arn
    desired_count = 3
    health_check_grace_period_seconds = 20
    launch_type = "FARGATE"
    deployment_minimum_healthy_percent = 100
    deployment_maximum_percent = 200
    scheduling_strategy = "REPLICA"

    network_configuration {
        subnets = module.vpc.private_subnets
        security_groups = [aws_security_group.api_app_sg.id]
        # assign_public_ip = true
    }

    load_balancer {
        target_group_arn = aws_lb_target_group.api_target_group.arn
        container_name = "${var.project_name}-users"
        container_port = 4000
    }
}

output "ecs_cluster_id" {
    value = aws_ecs_cluster.ecs_cluster.id
}