module "vpc" {
  	source  = "terraform-aws-modules/vpc/aws"
  	version = "3.13.0"

	# we can get the attributes of the module from the module source on https://registry.terraform.io/modules/terraform-aws-modules/vpc/aws/latest
	name = "${var.project_name}-vpc"
	cidr = var.vpc_cidr
	enable_dns_hostnames = true
	enable_dns_support = true

	azs             = ["us-east-1a", "us-east-1b", "us-east-1c"]
	public_subnets  = var.vpc_public_subnets_cidr
	
  	private_subnets = var.vpc_private_subnets_cidr
	enable_nat_gateway = true
	single_nat_gateway = true

	# Database subnets
	create_database_subnet_group = true
	create_database_subnet_route_table = true
	database_subnets = var.vpc_database_subnets_cidr
	create_database_nat_gateway_route = false
	create_database_internet_gateway_route = false

	public_subnet_tags = {
		Type: "public-subnets"
	}

	private_subnet_tags = {
		Type: "private-subnets"
	}

	database_subnet_tags = {
		Type: "database-subnets"
	}

	tags = {
		Owner: "Gabriel",
		Project: "${var.project_name}",
		Environment: "${var.environment}"
	}

	vpc_tags = {
		Name: "${var.project_name}-vpc"
		Framework = "Terraform"
	}
}

output "vpc_id" {
  description = "The ID of the VPC"
  value       = module.vpc.vpc_id
}

output "vpc_cidr_block" {
  description = "The CIDR block of the VPC"
  value       = module.vpc.vpc_cidr_block
}

output "public_subnets" {
  description = "List of IDs of public subnets"
  value       = module.vpc.public_subnets
}

output "private_subnets" {
  description = "List of IDs of private subnets"
  value       = module.vpc.private_subnets
}

output "private_database_subnets" {
  description = "List of IDs of private database subnets"
  value       = module.vpc.database_subnets
}

output "database_subnet_group_name" {
  description = "Database subnet group name"
  value       = module.vpc.database_subnet_group_name
}

output "nat_public_ips" {
  description = "List of public Elastic IPs created for AWS NAT Gateway"
  value       = module.vpc.nat_public_ips
}

output "azs" {
  description = "A list of availability zones spefified as argument to this module"
  value       = module.vpc.azs
}
