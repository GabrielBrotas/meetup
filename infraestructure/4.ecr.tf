resource "aws_ecr_repository" "users_api" {
    name = "${var.project_name}-users-api"

    image_scanning_configuration {
        scan_on_push = true
    }

    tags = {
        Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
    }
}

resource "aws_ecr_repository" "categories_api" {
    name = "${var.project_name}-categories-api"

    image_scanning_configuration {
        scan_on_push = true
    }

    tags = {
        Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
    }
}

resource "aws_ecr_repository" "meetings_api" {
    name = "${var.project_name}-meetings-api"

    image_scanning_configuration {
        scan_on_push = true
    }

    tags = {
        Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
    }
}

output "users_ecr_repository_arn" {
    value = aws_ecr_repository.users_api.arn
}

output "users_ecr_repository_url" {
    value = aws_ecr_repository.users_api.repository_url
}

output "categories_ecr_repository_arn" {
    value = aws_ecr_repository.categories_api.arn
}

output "categories_ecr_repository_url" {
    value = aws_ecr_repository.categories_api.repository_url
}

output "meetings_ecr_repository_arn" {
    value = aws_ecr_repository.meetings_api.arn
}

output "meetings_ecr_repository_url" {
    value = aws_ecr_repository.meetings_api.repository_url
}

