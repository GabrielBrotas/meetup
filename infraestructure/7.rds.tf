resource "aws_security_group" "api_rds_sg" {
    name = "${var.project_name}-api-rds-sg"
    description = "Allow traffic from api sg to database"
    vpc_id = module.vpc.vpc_id

    ingress = [
        {
            description = "Allow traffic from internet"
            from_port = 5432
            to_port = 5432
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
        Name = "${var.project_name}-categories-rds-sg"
        Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
    }
}

resource "aws_db_parameter_group" "categories" {
  name   = "categories"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "categories" {
  depends_on = [
    module.vpc
  ]
  identifier             = "categories"
  username               = "postgres"
  password               = "postgres123"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  max_allocated_storage  = 10
  engine                 = "postgres"
  engine_version         = "14.2"
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.api_rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.categories.name
  publicly_accessible    = false
  skip_final_snapshot    = true

  db_name = "meetupcategories"
}

resource "aws_db_parameter_group" "meetings" {
  name   = "meetings"
  family = "postgres14"

  parameter {
    name  = "log_connections"
    value = "1"
  }
}

resource "aws_db_instance" "meetings" {
  depends_on = [
    module.vpc
  ]
  identifier             = "meetings"
  username               = "postgres"
  password               = "postgres123"
  instance_class         = "db.t3.micro"
  allocated_storage      = 5
  max_allocated_storage  = 10
  engine                 = "postgres"
  engine_version         = "14.2"
  db_subnet_group_name   = module.vpc.database_subnet_group_name
  vpc_security_group_ids = [aws_security_group.api_rds_sg.id]
  parameter_group_name   = aws_db_parameter_group.categories.name
  publicly_accessible    = false
  skip_final_snapshot    = true

  db_name = "meetupmeetings"
}

output "categories_db_name" {
  description = "categories database name"
  value = aws_db_instance.categories.db_name
}

output "categories_db_endpoint" {
  description = "categories db endpoint"
  value = aws_db_instance.categories.endpoint
}

output "meetings_db_name" {
  description = "meetings database name"
  value = aws_db_instance.meetings.db_name
}

output "meetings_db_endpoint" {
  description = "meetings db endpoint"
  value = aws_db_instance.meetings.endpoint
}